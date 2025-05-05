from users.models import User, ACADEMIC_TITLE_SORT_ORDER
from django.db.models import Case, When, Value, IntegerField

class SearchService():
    @staticmethod
    def _annotate_academic_title_order(query_set):
        when_condition = [
            When(academic_title=key, then=Value(value))
            for key, value in ACADEMIC_TITLE_SORT_ORDER.items()
        ]

        return query_set.annotate(
            academic_title_order=Case(
                *when_condition,
                output_field=IntegerField(),
            )
        )

    def search_user(self, tags=None, department=None, limit=10, offset=0, sort_by=["academic_title"], orders=["desc"]):
        if sort_by is not None and len(sort_by) != len(orders):
            raise ValueError("Length of sort_by and orders must match.")
        
        results = User.objects.all()

        if department:
            results = results.filter(department__name__icontains=department)

        if sort_by:
            order_by_arguments = []
            for field, order in zip(sort_by, orders):
                if field == "academic_title":
                    results = self._annotate_academic_title_order(results)
                    field = "academic_title_order"

                if order == "desc":
                    order_by_arguments.append(f"-{field}")
                else:
                    order_by_arguments.append(field)

            results = results.order_by(*order_by_arguments)

        return results[offset:offset+limit]