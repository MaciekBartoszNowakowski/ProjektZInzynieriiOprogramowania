from rest_framework import serializers
from users.models import SupervisorProfile, User
from users.serializers.user_serializer import UserSerializer

class SupervisorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    bacherol_limit = serializers.IntegerField(required=False)
    engineering_limit = serializers.IntegerField(required=False)
    master_limit = serializers.IntegerField(required=False)
    phd_limit = serializers.IntegerField(required=False)

    class Meta:
        model = SupervisorProfile
        fields = [
            'user',
            'bacherol_limit',
            'engineering_limit',
            'master_limit',
            'phd_limit',
        ]