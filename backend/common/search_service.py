from users.models import User

class SearchService():
    def search_user(self, tags=None, department=None, limit=10, offset=0, sort_by=["department"], orders=["desc"]):
        if sort_by is not None and len(sort_by) != len(orders):
            raise ValueError("Length of sort_by and orders must match.")
        
        results = User.objects.all()

        if department:
            results = results.filter(department__name__icontains=department)

        if sort_by:
            order_by_arguments = []
            for field, order in zip(sort_by, orders):
                if order == "desc":
                    order_by_arguments.append(f"-{field}")
                else:
                    order_by_arguments.append(field)

            results = results.order_by(*order_by_arguments)

        return results[offset:offset+limit]