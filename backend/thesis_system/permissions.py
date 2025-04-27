from functools import wraps
from django.http import HttpResponseForbidden, HttpRequest
from users.models import User, Role
from rest_framework.permissions import BasePermission

class isStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.STUDENT
    
class isSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.SUPERVISOR

class isCoordinator(BasePermission):
    def has_permission(self, request, view):
         return request.user.is_authenticated and request.user.role == Role.COORDINATOR

class isAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role== Role.ADMIN
    
class isStudentOrSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role ==  Role.STUDENT or request.user.role == Role.SUPERVISOR)