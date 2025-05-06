from django.urls import path
from common.views.user_search_view import UserSearchView

urlpatterns = [
    path('search-users/', UserSearchView.as_view(), name='search-users')
]