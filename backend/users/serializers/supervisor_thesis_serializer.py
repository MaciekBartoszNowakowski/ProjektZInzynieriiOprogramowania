from rest_framework import serializers
from users.models import SupervisorProfile, User
from common.models import Tag, Department


class UserThesisSerializer(serializers.ModelSerializer):
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
            'email',
            'first_name',
            'last_name', 
            'academic_title',
            'description',
            'department',
            'department_name', 
            'tags'
        ]
        read_only_fields = [
            'email',
            'first_name',
            'last_name', 
            'academic_title',
            'description',
            'department',
            'department_name', 
            'tags'
        ]

class SupervisorThesisSerializer(serializers.ModelSerializer):
    user = UserThesisSerializer()

    class Meta:
        model = SupervisorProfile
        fields = ['user']
        read_only_fields = ['user']
