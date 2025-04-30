from django.urls import path
from .views import user_views

urlpatterns = [
    path('', user_views.get_user_profile_view, name='get_user_profile'),
    path('update', user_views.update_user_profile_view, name='update_user_profile'),
]