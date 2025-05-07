from rest_framework.generics import APIView, CreateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from thesis.services.thesis_service import ThesisService
from thesis.serializers.thesis_serializer import ThesisSerializer


class ThesisAddView(CreateAPIView):
    """
    Endpoint for adding new thesis by authenticated supervisor.
    Allows supervisors to add new thesis of different type.
    """
    permission_classes = [IsAuthenticated]

    def add_thesis(self, request):
        service = ThesisService()
        
        try:
            supervisor_id = request.POST.get("supervisor_id")
            thesis_type = request.POST.get("thesis_type"),
            name = request.POST.get("name"),
            description = request.POST.get("description"),
            max_students = request.POST.get("max_students"),
            language = request.POST.get("language")

            new_thesis = service.add_new_thesis(
                supervisor_id=supervisor_id,
                thesis_type=thesis_type,
                name=name,
                description=description,
                max_students=max_students,
                language=language
            )
        except Exception as e:
            raise ValidationError(str(e))
        
        serializer = ThesisSerializer(new_thesis)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class AvailableThesisView(APIView):
    """
    Endpoint for getting all available thesis.
    Allows users to browse thesis open for application.
    """
    def get_all_theses(self, request):
        service = ThesisService()
        
        try:
            theses = service.get_available_theses()
        except Exception as e:
            raise ValidationError(str(e))
        
        serializer = ThesisSerializer(theses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
