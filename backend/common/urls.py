from django.urls import path
from common.views.user_search_view import UserSearchView
from common.views.tag_list_view import TagListView

urlpatterns = [
    path('', TagListView.as_view(), name='tag-list'),
    path('search-users/', UserSearchView.as_view(), name='search-users')
]