from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from common.search_service import SearchService
from users.serializers.user_serializer import UserSerializer

class UserSearchView(APIView):
    def get(self, request):
        service = SearchService()

        try:
            first_name = request.GET.get("first_name")
            last_name = request.GET.get("last_name")
            tags = request.GET.getlist("tags") or None
            department = request.GET.get("department")
            role = request.GET.get("role")
            sort_by = request.GET.getlist("sort_by") or ["matching_tag_count",  "academic_title", "last_name", "first_name"]
            orders = request.GET.getlist("orders") or ["desc", "desc", "asc", "asc"]
            limit = int(request.GET.get("limit", 10))
            offset = int(request.GET.get("offset", 0))

            users = service.search_user(
                first_name=first_name,
                last_name=last_name,
                tags=tags,
                department=department,
                role=role,
                sort_by=sort_by,
                orders=orders,
                limit=limit,
                offset=offset,
            )
        except ValueError as e:
            raise ValidationError(str(e))
        
        serializer = UserSerializer(users, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)