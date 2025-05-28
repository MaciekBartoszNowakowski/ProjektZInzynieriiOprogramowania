from rest_framework import serializers
from thesis.models import Thesis
from users.models import StudentProfile
from applications.models import Submission


class ThesisMinimalSerializer(serializers.ModelSerializer):
    supervisor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Thesis
        fields = [
            'id', 'name', 'thesis_type', 'description', 
            'status', 'language', 'supervisor_name'
        ]
    
    def get_supervisor_name(self, obj):
        supervisor = obj.supervisor_id.user
        title = supervisor.academic_title if supervisor.academic_title != 'brak' else ''
        full_name = supervisor.get_full_name()
        return f"{title} {full_name}".strip()
