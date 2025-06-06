from rest_framework import serializers
from thesis.models import Thesis
from users.models import StudentProfile
from applications.models import Submission

class StudentMinimalSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentProfile
        fields = ['index_number', 'full_name', 'url']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    
    def get_url(self, obj):
        request = self.context.get('request')

        return request.build_absolute_uri(f'/users/{obj.user.id}')