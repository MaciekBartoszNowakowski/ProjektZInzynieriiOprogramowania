from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError 

from thesis_system.permissions import isCoordinator 
from users.models import User, Role, StudentProfile, SupervisorProfile
from users.serializers.single_user_create_serializer import SingleUserCreateSerializer
from users.serializers.user_serializer import UserSerializer
from users.serializers.student_serializer import StudentProfileSerializer
from users.serializers.supervisor_serializer import SupervisorProfileSerializer
from users.services.account_creation_service import account_service 

class UserCreateView(CreateAPIView):
    serializer_class = SingleUserCreateSerializer 
    permission_classes = [IsAuthenticated, isCoordinator] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        requesting_user = self.request.user

        user_department = requesting_user.department 
        if not user_department:
             raise PermissionDenied("Twoje konto użytkownika nie jest przypisane do żadnego działu, co uniemożliwia tworzenie nowych kont.")

        created_user = None 

        validated_data = serializer.validated_data

        try:
            created_user = account_service.create_single_user(
                 coordinator=requesting_user, 
                 validated_data=validated_data, 
            )

        except ValueError as e:
            raise ValidationError({'detail': str(e)}) 
        except Exception as e:
             raise status.HTTP_500_INTERNAL_SERVER_ERROR

        output_serializer = None
        if created_user.role == Role.STUDENT:
            output_serializer = StudentProfileSerializer(created_user.studentprofile) 
        else:
            output_serializer = SupervisorProfileSerializer(created_user.supervisorprofile) 
        
        headers = self.get_success_headers(output_serializer.data) 
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)