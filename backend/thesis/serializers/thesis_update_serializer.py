from rest_framework import serializers
from thesis.models import Thesis
from common.models import Tag


class ThesisUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
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
            'thesis_type'
        ]
