from django.urls import path
from .views.user_views import ProfileView

urlpatterns = [
    path('me/', ProfileView.as_view(), name='my-profile'),
]