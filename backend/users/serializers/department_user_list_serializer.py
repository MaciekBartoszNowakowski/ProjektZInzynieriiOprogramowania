from rest_framework import serializers
from users.models import User

class DepartmentUserListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='coordinator-user-detail', 
        lookup_field='pk'
    )

    class Meta:
        model = User
        fields = [
            'url',
            'academic_title',
            'first_name',
            'last_name', 
            'email',
            'role',
            'is_active',
        ]
        read_only_fields = [
            'url',
            'academic_title',
            'first_name',
            'last_name', 
            'email',
            'role',
            'is_active',
        ]