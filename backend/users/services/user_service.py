from rest_framework.response import Response
from rest_framework import status
from users.models import User, Role
from users.serializers.student_serializer import StudentProfileSerializer
from users.serializers.supervisor_serializer import SupervisorProfileSerializer
from users.serializers.user_serializer import UserSerializer
from rest_framework.request import Request

def get_user_profile_data(user: User) -> Response:
    if user.role == Role.STUDENT:
        try:
            serializer = StudentProfileSerializer(user.studentprofile)
        except user.studentprofile.RelatedObjectDoesNotExist:
            return Response({"detail": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)
    elif user.role == Role.SUPERVISOR:
        try:
            serializer = SupervisorProfileSerializer(user.supervisorprofile)
        except user.supervisorprofile.RelatedObjectDoesNotExist:
             return Response({"detail": "Supervisor profile not found."}, status=status.HTTP_404_NOT_FOUND)
    elif user.role in [Role.COORDINATOR, Role.ADMIN]:
        serializer = UserSerializer(user)
    else:
        serializer = UserSerializer(user)

    return Response(serializer.data)

def update_user_profile_data(user: User, request: Request) -> Response:
    if user.role == Role.STUDENT:
        try:
            serializer = StudentProfileSerializer(user.studentprofile, data=request.data, partial=request.method == 'PATCH')
        except user.studentprofile.RelatedObjectDoesNotExist:
            return Response({"detail": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)
    elif user.role == Role.SUPERVISOR:
        try:
            serializer = SupervisorProfileSerializer(user.supervisorprofile, data=request.data, partial=request.method == 'PATCH')
        except user.supervisorprofile.RelatedObjectDoesNotExist:
             return Response({"detail": "Supervisor profile not found."}, status=status.HTTP_404_NOT_FOUND)
    elif user.role in [Role.COORDINATOR, Role.ADMIN]:
         serializer = UserSerializer(user, data=request.data, partial=request.method == 'PATCH')
    else:
        serializer = UserSerializer(user, data=request.data, partial=request.method == 'PATCH')

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)