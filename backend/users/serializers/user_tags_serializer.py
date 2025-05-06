from rest_framework import serializers
from common.models import Tag

class TagsUpdateSerializer(serializers.Serializer):
    to_add = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all()),
        required=False,     
        allow_empty=True 
    )

    to_remove = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all()),
        required=False,     
        allow_empty=True 
    )
