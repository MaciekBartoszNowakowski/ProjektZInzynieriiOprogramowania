from rest_framework import serializers
from thesis.models import Thesis


class ThesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thesis

        # tutaj można zmienić tylko opis
        fields = [
            'id',
            'supervisor_id',
            'thesis_type',
            'name',
            'description',
            'max_students',
            'language'
        ]
        read_only_fields = [
            'id',
            'supervisor_id',
            'thesis_type',
            'name',
            'max_students',
            'language'
        ]
