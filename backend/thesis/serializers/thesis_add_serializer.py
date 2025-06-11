from rest_framework import serializers
from thesis.models import ThesisType
from common.models import Tag


class ThesisAddSerializer(serializers.Serializer):
    thesis_type = serializers.ChoiceField(
        choices=ThesisType.choices,
        required=True
    )
    name = serializers.CharField(
        max_length=100, 
        required=True
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True
    )
    max_students = serializers.IntegerField(
        min_value=1, 
        required=False
    )
    language = serializers.CharField(
        max_length=100, 
        required=False
    )
    tags = serializers.MultipleChoiceField(
        choices = [] if Tag.objects is None else Tag.objects.all(),
        required=False
    )
