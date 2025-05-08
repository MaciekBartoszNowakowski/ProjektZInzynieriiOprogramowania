from rest_framework import serializers
from common.models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        
        fields = [
            'name',
            'description'
        ]