from rest_framework import serializers
from common.models import Department

class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'description'
        ]
        read_only_fields = [
            'id',
            'name',
            'description'
        ]