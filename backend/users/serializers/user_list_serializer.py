from rest_framework import serializers
from users.models import User

class UserListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail', 
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
        ]
        read_only_fields = [
            'url',
            'academic_title',
            'first_name',
            'last_name', 
            'email',
            'role',
        ]