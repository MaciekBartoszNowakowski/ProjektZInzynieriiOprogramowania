from rest_framework import serializers
from users.models import User
from common.models import Tag

class UserSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = User
        #zakładamy że tutaj user może edytować tylko opis, tagi w osobnych endpointach
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
            'tags'
        ]