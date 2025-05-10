from rest_framework import serializers
from thesis.models import Thesis


class ThesisListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='available-theses-detail', 
        lookup_field='pk'
    )

    class Meta:
        model = Thesis
        fields = [
            'url',
            'supervisor_id',
            'thesis_type',
            'name',
            'description',
            'max_students',
            'language'
        ]
        read_only_fields = [
            'url',
            'supervisor_id',
            'thesis_type',
            'name',
            'description',
            'max_students',
            'language'
        ]
