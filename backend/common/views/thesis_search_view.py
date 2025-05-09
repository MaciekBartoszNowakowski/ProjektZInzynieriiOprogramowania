from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from common.search_service import SearchService
from thesis.serializers.thesis_list_serializer import ThesisListSerializer

class ThesisSearchView(APIView):
    """
        Endpoint for filtering available theses.
    """
    def get(self, request):
        service = SearchService()

        try:
            first_name = request.GET.get("first_name")
            last_name = request.GET.get("last_name")
            academic_title = request.GET.get("academic_title")
            tags = request.GET.getlist("tags") or None
            department = request.GET.get("department")
            thesis_type = request.GET.get("thesis_type")
            language = request.GET.get("language")
            limit = int(request.GET.get("limit", 10))
            offset = int(request.GET.get("offset", 0))

            theses = service.search_topics(
                first_name=first_name,
                last_name=last_name,
                academic_title=academic_title,
                tags=tags,
                department=department,
                thesis_type=thesis_type,
                language=language,
                limit=limit,
                offset=offset,
            )
        except ValueError as e:
            raise ValidationError(str(e))
        
        serializer = ThesisListSerializer(theses, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
