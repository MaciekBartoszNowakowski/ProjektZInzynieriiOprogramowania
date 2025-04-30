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

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        profile_instance = super().update(instance, validated_data)

        if user_data:
            user_instance = profile_instance.user 

            if 'description' in user_data:
                new_description = user_data['description']
                user_instance.description = new_description
                user_instance.save() 

        return profile_instance 