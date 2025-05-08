from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from common.serializers.tag_serializer import TagSerializer
from users.serializers.user_tags_serializer import TagsUpdateSerializer
from users.services.user_service import user_service


class UpdateTagsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_tags = user.tags.all()
        serializer = TagSerializer(user_tags, many=True)
        
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = TagsUpdateSerializer(data=request.data, context={'request': request})
        
        try:
            serializer.is_valid(raise_exception=True)
            updated_tags = user_service.update_user_tags(user, serializer.validated_data)
            response_serializer = TagSerializer(updated_tags, many=True)
            
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
             raise
        except Exception as e:
             return Response({'detail': 'Wystąpił nieoczekiwany błąd serwera podczas aktualizacji tagów.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)