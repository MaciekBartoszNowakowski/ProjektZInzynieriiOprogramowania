from users.models import User, ACADEMIC_TITLE_SORT_ORDER, Role, SupervisorProfile, AcademicTitle
from thesis.models import Thesis, ThesisStatus, ThesisType, THESIS_TYPE_SORT_ORDER
from django.db.models import Case, When, Value, IntegerField, Q, Count

class SearchService():
    @staticmethod
    def _annotate_academic_title_order(queryset):
        when_condition = [
            When(academic_title=key, then=Value(value))
            for key, value in ACADEMIC_TITLE_SORT_ORDER.items()
        ]

        return queryset.annotate(
            academic_title_order=Case(
                *when_condition,
                output_field=IntegerField(),
            )
        )
    
    @staticmethod
    def _annotate_supervisor_title_order(queryset):
        when_condition = [
            When(supervisor_id__user__academic_title=key, then=Value(value))
            for key, value in ACADEMIC_TITLE_SORT_ORDER.items()
        ]

        return queryset.annotate(
            supervisor_title_order=Case(
                *when_condition,
                output_field=IntegerField()
            )
        )
    
    @staticmethod
    def _annotate_thesis_type_order(queryset):
        when_condition = [
            When(thesis_type=key, then=Value(value))
            for key, value in THESIS_TYPE_SORT_ORDER.items()
        ]

        return queryset.annotate(
            thesis_type_order=Case(
                *when_condition,
                output_field=IntegerField()
            )
        )
    
    @staticmethod
    def _filter_by_tags(queryset, tags: list[str]):
        query = Q()
        for tag in tags:
            query |= Q(tags__name=tag)

        return queryset.filter(query).distinct()
    
    @staticmethod
    def _annotate_tag_count(queryset, tags: list[str]):
        return queryset.annotate(
            matching_tag_count=Count(
                'tags',
                filter=Q(tags__name__in=tags),
                distinct=True
            )
        )
    
    def __search_all_match(
        self, 
        first_name,
        last_name,
        tags, 
        department, 
        role,
        sort_by, 
        orders,
    ):
        if sort_by is not None and len(sort_by) != len(orders):
            raise ValueError("Length of sort_by and orders must be of the same length")
        
        results = User.objects.all()

        if role:
            try:
                role_value = Role[role.upper()].value
            except KeyError:
                raise ValueError(f"Unknown role: {role}")
            
            results = results.filter(role=role_value)

        if first_name:
            results = results.filter(first_name=first_name)

        if last_name:
            results = results.filter(last_name=last_name)

        if department:
            results = results.filter(department__name=department)

        if tags:
            results = self._filter_by_tags(results, tags)

        if sort_by:
            order_by_arguments = []
            for field, order in zip(sort_by, orders):
                if field == "academic_title":
                    results = self._annotate_academic_title_order(results)
                    field = "academic_title_order"

                if tags and field == "matching_tag_count":
                    results = self._annotate_tag_count(results, tags)
                elif field == "matching_tag_count":
                    continue

                if order == "desc":
                    order_by_arguments.append(f"-{field}")
                else:
                    order_by_arguments.append(field)

            results = results.order_by(*order_by_arguments)

        return results

    def search_user(
        self, 
        first_name=None,
        last_name=None,
        tags=None, 
        department=None, 
        role=None,
        sort_by=["academic_title"], 
        orders=["desc"], 
        limit=10, 
        offset=0,
    ):
        if limit < 0 or offset < 0:
            raise ValueError(f"Limit and offset must be non-negative integers")

        all_results = self.__search_all_match(
            first_name=first_name, 
            last_name=last_name,
            tags=tags,
            department=department,
            role=role,
            sort_by=sort_by,
            orders=orders,
        )

        return all_results[offset:offset+limit]
    
    def search_topics(
        self, 
        first_name=None,
        last_name=None,
        academic_title=None,
        tags=None, 
        department=None, 
        thesis_type=None,
        language=None,
        limit=10, 
        offset=0,
    ):
        if limit < 0 or offset < 0:
            raise ValueError(f"Limit and offset must be non-negative integers")

        supervisors = self.__search_all_match(
            first_name=first_name, 
            last_name=last_name,
            tags=tags,
            department=department,
            role="supervisor",
            sort_by=None, # not applicable
            orders=None # not applicable
        )

        supervisors = SupervisorProfile.objects.filter(user_id__in=supervisors)
        topics = Thesis.objects.filter(supervisor_id__in=supervisors)
        topics = topics.filter(status=ThesisStatus.APP_OPEN)

        order_by_arguments = []

        if academic_title:
            try:
                academic_title_value = AcademicTitle[academic_title.upper()].value
            except KeyError:
                raise ValueError(f"Unknown academic title: {academic_title}")
            
            topics = topics.filter(supervisor_id__user__academic_title=academic_title_value)
        else:
            topics = self._annotate_supervisor_title_order(topics)
            order_by_arguments.append("-supervisor_title_order")

        if thesis_type:
            try:
                thesis_type_value = ThesisType[thesis_type.upper()].value
            except KeyError:
                raise ValueError(f"Unknown thesis type: {thesis_type}")
            
            topics = topics.filter(thesis_type=thesis_type_value)
        else:
            topics = self._annotate_thesis_type_order(topics)
            order_by_arguments.append('-thesis_type_order')

        if language:
            topics = topics.filter(language=language)

        if order_by_arguments:
            topics = topics.order_by(*order_by_arguments)
        return topics[offset:offset+limit]
