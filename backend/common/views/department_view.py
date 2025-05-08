from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from common.models import Department
from common.serializers.department_serializer import DepartmentSerializer
from thesis_system.permissions import isCoordinator
from common.services.department_service import department_service

class DepartmentView(RetrieveUpdateAPIView):
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), isCoordinator()]
        return [IsAuthenticated()]

    def get_object(self):
        user = self.request.user
        return Department.objects.get(pk=user.department_id)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_department = department_service.update_department(
            coordinator=request.user,
            validated_data=serializer.validated_data
        )

        output_serializer = self.get_serializer(updated_department)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
