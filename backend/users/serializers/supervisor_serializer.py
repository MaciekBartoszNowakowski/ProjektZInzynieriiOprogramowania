from rest_framework import serializers
from users.models import SupervisorProfile, User
from users.serializers.user_serializer import UserSerializer

class SupervisorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SupervisorProfile
        fields = [
            'user',
            'bacherol_limit',
            'engineering_limit',
            'master_limit',
            'phd_limit',
        ]