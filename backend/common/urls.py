from django.urls import path
from common.views.user_search_view import UserSearchView
from common.views.tag_list_view import TagListView
from common.views.department_view import DepartmentView

urlpatterns = [
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('search-users/', UserSearchView.as_view(), name='search-users'),
    path('department/', DepartmentView.as_view(), name='department-view')
]