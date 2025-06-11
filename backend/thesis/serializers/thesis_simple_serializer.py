from rest_framework import serializers
from thesis.models import Thesis


class ThesisSimpleSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Thesis
        fields = [
            'id',
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
            'thesis_type',
            'name',
            'description',
            'max_students',
            'status',
            'language',
            'tags'
        ]
