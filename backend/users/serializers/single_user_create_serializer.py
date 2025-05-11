from rest_framework import serializers
from users.models import Role, AcademicTitle


class SingleUserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True
    )
    first_name = serializers.CharField(
        max_length=150, 
        required=True
    )
    last_name = serializers.CharField(
        max_length=150, 
        required=True
    )
    academic_title = serializers.ChoiceField(
        choices=AcademicTitle.choices, 
        required=True
    )
    role = serializers.ChoiceField(
        choices=[Role.STUDENT, Role.SUPERVISOR], 
        required=True
    )
    index_number = serializers.CharField(
        max_length=6, 
        required=False, 
        allow_blank=True
    )