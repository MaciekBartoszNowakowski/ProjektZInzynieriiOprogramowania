from applications.serializers.student_minimal_serializer import StudentMinimalSerializer
from applications.serializers.thesis_minimal_serializer import ThesisMinimalSerializer
from rest_framework import serializers
from thesis.models import Thesis
from users.models import StudentProfile
from applications.models import Submission

class CreatedSubmissionSerializer(serializers.ModelSerializer):
    student = StudentMinimalSerializer(read_only=True)
    thesis = ThesisMinimalSerializer(read_only=True)
    
    class Meta:
        model = Submission
        fields = ['id', 'student', 'thesis']
