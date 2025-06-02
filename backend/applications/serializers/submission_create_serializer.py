from rest_framework import serializers
from thesis.models import Thesis
from users.models import StudentProfile
from applications.models import Submission

class SubmissionCreateSerializer(serializers.Serializer):
    thesis_id = serializers.IntegerField()
    
    def validate_thesis_id(self, value):
        if not Thesis.objects.filter(id=value).exists():
            raise serializers.ValidationError("Thesis with given ID does not exist")
        return value