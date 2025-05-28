from applications.serializers.submission_serializer import SubmissionSerializer
from rest_framework import serializers
from thesis.models import Thesis
from users.models import StudentProfile
from applications.models import Submission

class SubmissionStatusSerializer(serializers.Serializer):
    has_submission = serializers.BooleanField()
    submission = SubmissionSerializer(required=False, allow_null=True)
    message = serializers.CharField(required=False)