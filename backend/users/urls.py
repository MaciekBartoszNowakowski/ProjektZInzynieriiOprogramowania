from django.urls import path
from users.views.profile_view import ProfileView
from users.views.users_view import UserListViewSet
from users.views.tags_update_view import UpdateTagsView
from users.views.create_user_view import UserCreateView

urlpatterns = [
    path('', UserListViewSet.as_view({'get': 'list'}), name='user-list'),
    path('<int:pk>/', UserListViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('me/', ProfileView.as_view(), name='my-profile'),
    path('me/tags/', UpdateTagsView.as_view(), name='update-tags'),
    path('create/', UserCreateView.as_view(), name='create-single-user'),
]