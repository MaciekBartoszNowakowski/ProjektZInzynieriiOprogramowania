from rest_framework.generics import ListAPIView

from common.models import Tag
from common.serializers.tag_serializer import TagSerializer

class TagListView(ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = []
    serializer_class = TagSerializer