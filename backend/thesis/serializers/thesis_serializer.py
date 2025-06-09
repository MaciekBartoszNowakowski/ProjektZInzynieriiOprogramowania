from rest_framework import serializers
from thesis.models import Thesis
from users.serializers.supervisor_thesis_serializer import SupervisorThesisSerializer


class ThesisSerializer(serializers.ModelSerializer):
    supervisor_id = SupervisorThesisSerializer()
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
            'thesis_type'
        ]
