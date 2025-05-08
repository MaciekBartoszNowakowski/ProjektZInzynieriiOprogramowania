from rest_framework import serializers
from users.models import User

class DepartmentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'academic_title',
            'first_name',
            'last_name', 
            'email',
            'role',
            'is_active',
        ]