from rest_framework import serializers
from thesis.models import Thesis


class ThesisUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thesis
        fields = [
            'id',
            'supervisor_id',
            'thesis_type',
            'name',
            'description',
            'max_students',
            'status',
            'language'
        ]
        read_only_fields = [
            'id',
            'supervisor_id',
            'thesis_type'
        ]
