from users.models import User, ACADEMIC_TITLE_SORT_ORDER, Role
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

        return results[offset:offset+limit]