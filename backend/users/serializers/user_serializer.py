from rest_framework import serializers
from users.models import User
from common.models import Tag, Department

class UserSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    department_name = serializers.SerializerMethodField() 

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None 

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name', 
            'academic_title',
            'role',
            'description',
            'department',
            'department_name', 
            'tags'
        ]
        read_only_fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'academic_title',
            'role',
            'department',
            'department_name', 
            'tags'
        ]
