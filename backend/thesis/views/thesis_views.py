from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status, viewsets
from django.db.models import Q 

from thesis.models import Thesis, ThesisStatus
from thesis_system.permissions import isSupervisor 
from thesis.services.thesis_service import ThesisService
from thesis.serializers.thesis_add_serializer import ThesisAddSerializer
from thesis.serializers.thesis_update_serializer import ThesisUpdateSerializer
from thesis.serializers.thesis_list_serializer import ThesisListSerializer
from thesis.serializers.thesis_simple_serializer import ThesisSimpleSerializer
from thesis.serializers.thesis_serializer import ThesisSerializer


class ThesisAddView(CreateAPIView):
    """
    Endpoint for adding new thesis by authenticated supervisor.
    Allows supervisors to add new thesis of different type.
    """
    serializer_class = ThesisAddSerializer
    permission_classes = [IsAuthenticated, isSupervisor]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        supervisor = self.request.user
        service = ThesisService()
        
        try:
            service.add_new_thesis(
                supervisor=supervisor,
                validated_data=validated_data
            )
        except Exception as e:
            return Response({ "detail": str(e) }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({ "detail": "New thesis added successfully." }, status=status.HTTP_201_CREATED)

    
class AvailableThesisView(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint for getting available theses.
    Allows users to browse theses open for application.
    """
    queryset = Thesis.objects.filter(Q(status=ThesisStatus.APP_OPEN))
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.action == 'list':
            return ThesisListSerializer
        return ThesisSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset
    

class ThesisUpdateView(UpdateAPIView):
    """
    Endpoint for updating thesis by supervisor who added it.
    Allows supervisors to update name, description, max_students, status and language.
    """
    serializer_class = ThesisUpdateSerializer
    permission_classes = [IsAuthenticated, isSupervisor]

    def update(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        supervisor = self.request.user
        service = ThesisService()
        
        try:
            updated_thesis = service.update_thesis(
                supervisor=supervisor,
                thesis_pk=pk,
                validated_data=validated_data
            )
        except Exception as e:
            return Response({ "detail": str(e) }, status=status.HTTP_400_BAD_REQUEST)
        
        output_serializer = ThesisUpdateSerializer(updated_thesis)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    

class ThesisDeleteView(DestroyAPIView):
    """
    Endpoint for deleting thesis by supervisor who added it.
    """
    permission_classes = [IsAuthenticated, isSupervisor]

    def delete(self, request, pk):
        supervisor = self.request.user
        service = ThesisService()
        
        try:
            deleted_thesis = service.delete_thesis(
                supervisor=supervisor,
                thesis_pk=pk,
            )
        except Exception as e:
            return Response({ "detail": str(e) }, status=status.HTTP_400_BAD_REQUEST)
        
        output_serializer = ThesisUpdateSerializer(deleted_thesis)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    

class NoThesisFoundException(APIException):
    status_code = status.HTTP_204_NO_CONTENT
    default_detail = 'Promotor nie ma żadnej pracy w systemie.'


class NoSupervisorFoundException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class SupervisorThesisView(ListAPIView):
    """
    Endpoint for getting all theses by supervisor who created them.
    """
    serializer_class = ThesisSimpleSerializer
    permission_classes = [IsAuthenticated, isSupervisor]

    def get_queryset(self):
        supervisor = self.request.user
        service = ThesisService()

        try:
            promotor_theses = service.get_promotor_theses(supervisor=supervisor)
        except Exception as e:
            raise NoSupervisorFoundException(str(e))
        
        if not promotor_theses:
            raise NoThesisFoundException()
        return promotor_theses
