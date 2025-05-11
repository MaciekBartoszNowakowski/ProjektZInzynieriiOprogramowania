from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q 

from users.serializers.user_serializer import UserSerializer
from users.serializers.user_list_serializer import UserListSerializer
from users.models import User, Role, StudentProfile, SupervisorProfile


class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter((Q(role=Role.STUDENT) | Q(role=Role.SUPERVISOR)) & Q(is_active=True))
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset