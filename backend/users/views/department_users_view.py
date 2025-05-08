from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError

from thesis_system.permissions import isCoordinator
from users.serializers.department_user_list_serializer import DepartmentUserListSerializer
from users.serializers.department_user_serializer import DepartmentUserSerializer
from users.models import User, Role
from users.services.coordinator_service import coordinator_service


class DepartmentUserListViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentUserListSerializer
    permission_classes = [IsAuthenticated, isCoordinator]

    def get_queryset(self):
        user = self.request.user
        if not user.department:
            return User.objects.none()
        return User.objects.filter(
            Q(role__in=[Role.STUDENT, Role.SUPERVISOR]),
            department=user.department
        )

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update', 'retrieve']:
            return DepartmentUserSerializer
        return DepartmentUserListSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)

            updated_user = coordinator_service.update_department_user(
                coordinator=request.user,
                user=instance,
                validated_data=serializer.validated_data
            )

            response_serializer = self.get_serializer(updated_user)
            return Response(response_serializer.data)

        except ValueError as e:
            raise ValidationError({'detail': str(e)})
        except PermissionDenied:
            raise
        except NotFound:
            raise
        except Exception:
            return Response(
                {'detail': 'Wystąpił nieoczekiwany błąd serwera podczas aktualizacji użytkownika działu.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            updated_user = coordinator_service.update_department_user(
                coordinator=request.user,
                user=instance,
                validated_data=serializer.validated_data
            )

            response_serializer = self.get_serializer(updated_user)
            return Response(response_serializer.data)

        except ValueError as e:
            raise ValidationError({'detail': str(e)})
        except PermissionDenied:
            raise
        except NotFound:
            raise
        except Exception:
            return Response(
                {'detail': 'Wystąpił nieoczekiwany błąd serwera podczas częściowej aktualizacji użytkownika działu.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
