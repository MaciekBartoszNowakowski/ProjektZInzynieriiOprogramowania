from rest_framework import serializers
from django.db import transaction
from users.models import SupervisorProfile, User
from users.serializers.user_serializer import UserSerializer # Assuming UserSerializer is here

class SupervisorProfileSerializer(serializers.ModelSerializer):
    # User field is now editable via nesting, just like in StudentProfileSerializer
    user = UserSerializer() # Removed read_only=True

    class Meta:
        model = SupervisorProfile
        fields = [
            'user', # Nested user data will be expected for updates
            'bacherol_limit',
            'engineering_limit',
            'master_limit',
            'phd_limit',
            # Removed user_description explicit field
        ]
        # Limits are editable by default unless added to read_only_fields
        # read_only_fields = ['bacherol_limit', 'engineering_limit', 'master_limit', 'phd_limit']


    def update(self, instance, validated_data):
        # Pop the nested user data first
        user_data = validated_data.pop('user', None)

        # Call the parent update method to handle SupervisorProfile's own fields (limits)
        # validated_data now only contains data for SupervisorProfile fields
        profile_instance = super().update(instance, validated_data)

        # If user data was provided and contains description, update the related User instance
        if user_data:
            user_instance = profile_instance.user # Get the related User instance

            # Check if description is in the provided user data
            if 'description' in user_data:
                new_description = user_data['description']

                # Update the user's description and save it
                # Using transaction.atomic() for safety, though APITestCase handles this
                with transaction.atomic():
                    user_instance.description = new_description
                    user_instance.save()

        return profile_instance
