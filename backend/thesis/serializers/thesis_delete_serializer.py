from rest_framework import serializers
from thesis.models import Thesis


class ThesisDeleteSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

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
            'language',
            'tags'
        ]
        read_only_fields = [
            'id',
            'supervisor_id',
            'thesis_type',
            'name',
            'description',
            'max_students',
            'status',
            'language',
            'tags'
        ]
