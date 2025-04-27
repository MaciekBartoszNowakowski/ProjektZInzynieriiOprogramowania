from django.urls import path
from . import views 

urlpatterns = [
    path('hello-all/', views.hello_world_view, name='hello_world'),
    path('hello-student/', views.hello_world_view_student_only, name='hello_world_student'),
    path('hello-supervisor/', views.hello_world_view_supervisor_only, name='hello_world_supervisor'),
    path('hello-coordinator/', views.hello_world_view_coordinator_only, name='hello_world_coordinator'),
    path('hello-admin/', views.hello_world_view_admin_only, name='hello_world_admin'),
    path('hello-student-or-supervisor/', views.hello_world_view_student_or_supervisor, name='hello_world_student_or_supervisor'),
]