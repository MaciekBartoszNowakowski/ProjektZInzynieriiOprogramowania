from rest_framework import serializers
from thesis.models import Thesis


class ThesisPromotorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thesis
        fields = [
            'id',
            'thesis_type',
            'name',
            'description',
            'max_students',
            'status',
            'language'
        ]
        read_only_fields = [
            'id',
            'thesis_type',
            'name',
            'description',
            'max_students',
            'status',
            'language'
        ]
