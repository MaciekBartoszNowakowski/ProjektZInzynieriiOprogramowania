from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.services.user_service import get_user_profile_data, update_user_profile_data 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile_view(request: Request) -> Response:
    return get_user_profile_data(request.user)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile_view(request: Request) -> Response:
    return update_user_profile_data(request.user, request)