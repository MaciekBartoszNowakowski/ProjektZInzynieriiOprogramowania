from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from common.models import Department
from common.serializers.department_list_serializer import DepartmentListSerializer

class DepartmentListView(ListAPIView):
    queryset = Department.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DepartmentListSerializer
