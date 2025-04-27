from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from thesis_system.permissions import isStudent, isSupervisor, isCoordinator, isAdmin, isStudentOrSupervisor

@api_view(['GET'])
@permission_classes([])
def hello_world_view(request: Request) -> Response:
    """
    A simple view that returns a hello message. Accessible by anyone.
    """
    data = {
        "message": "Hello from Django!",
        "status": "success",
        "data": {
            "greeting": "Hello, World!"
        }
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([isStudent])
def hello_world_view_student_only(request: Request) -> Response:
    """
    A view accessible only by users with the 'student' role.
    """
    data = {
        "message": "Hello from Django!",
        "status": "success",
        "data": {
            "greeting": "Hello, Student!"
        }
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([isSupervisor])
def hello_world_view_supervisor_only(request: Request) -> Response:
    """
    A view accessible only by users with the 'supervisor' role.
    """
    data = {
        "message": "Hello from Django!",
        "status": "success",
        "data": {
            "greeting": "Hello, Supervisor!"
        }
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([isCoordinator])
def hello_world_view_coordinator_only(request: Request) -> Response:
    """
    A view accessible only by users with the 'coordinator' role.
    """
    data = {
        "message": "Hello from Django!",
        "status": "success",
        "data": {
            "greeting": "Hello, Coordinator!"
        }
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([isAdmin])
def hello_world_view_admin_only(request: Request) -> Response:
    """
    A view accessible only by users with the 'admin' role.
    """
    data = {
        "message": "Hello from Django!",
        "status": "success",
        "data": {
            "greeting": "Hello, Admin!"
        }
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([isStudentOrSupervisor])
def hello_world_view_student_or_supervisor(request: Request) -> Response:
    """
    A view accessible only by users with either 'student' or 'supervisor' roles.
    """
    data = {
        "message": "Hello from Django!",
        "status": "success",
        "data": {
            "greeting": "Hello, Student or Supervisor!"
        }
    }
    return Response(data)
