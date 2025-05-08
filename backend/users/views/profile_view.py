from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from drf_spectacular.utils import extend_schema, OpenApiResponse, PolymorphicProxySerializer

from users.models import User, Role, StudentProfile, SupervisorProfile
from users.serializers.user_serializer import UserSerializer
from users.serializers.student_serializer import StudentProfileSerializer
from users.serializers.supervisor_serializer import SupervisorProfileSerializer
from users.services.user_service import user_service


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if user.role == Role.STUDENT:
            try:
                return user.studentprofile
            except StudentProfile.DoesNotExist:
                raise NotFound("Student profile does not exist for this user.")
        elif user.role == Role.SUPERVISOR:
            try:
                return user.supervisorprofile
            except SupervisorProfile.DoesNotExist:
                raise NotFound("Supervisor profile does not exist for this user.")
        else:
            return user

    def get_serializer_class(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return UserSerializer
        if user.role == Role.STUDENT:
            return StudentProfileSerializer
        elif user.role == Role.SUPERVISOR:
            return SupervisorProfileSerializer
        elif user.role in [Role.COORDINATOR, Role.ADMIN]:
             return UserSerializer
        else:
             raise NotImplementedError(f"Serializer for role '{user.role}' is not defined in ProfileView.")


    def perform_update(self,
                       serializer: serializers.Serializer
                      ):
        instance_to_update = serializer.instance
        validated_data = serializer.validated_data
        user_instance = instance_to_update.user if hasattr(instance_to_update, 'user') else instance_to_update
        updated_user_instance = user_service.update_user_data(
            user = user_instance,
            validated_data = validated_data
        )
        if user_instance.role == Role.STUDENT:
             updated_user_instance.studentprofile.refresh_from_db()
             return updated_user_instance.studentprofile
        elif user_instance.role == Role.SUPERVISOR:
            updated_user_instance.supervisorprofile.refresh_from_db()
            return updated_user_instance.supervisorprofile
        elif user_instance.role in [Role.COORDINATOR, Role.ADMIN]:
            updated_user_instance.refresh_from_db()
            return updated_user_instance
        else:
             raise NotImplementedError(f"Update logic for role '{user_instance.role}' is not defined in ProfileView.")


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance_for_response = self.perform_update(serializer)
            response_serializer = self.get_serializer(updated_instance_for_response)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
             raise ValidationError({'detail': str(e)})
        except NotFound:
             raise
        except PermissionDenied:
             raise
        except Exception as e:
             return Response({'detail': 'Wystąpił nieoczekiwany błąd serwera.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)