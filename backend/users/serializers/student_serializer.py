from rest_framework import serializers
from users.models import StudentProfile, User
from users.serializers.user_serializer import UserSerializer

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer() 

    class Meta:
        model = StudentProfile
        fields = [
            'user',
            'index_number', 
        ]
        read_only_fields = ['index_number']