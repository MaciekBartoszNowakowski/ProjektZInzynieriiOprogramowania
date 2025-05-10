from django.urls import path
from common.views.user_search_view import UserSearchView
from common.views.tag_list_view import TagListView
from common.views.department_view import DepartmentView
from common.views.thesis_search_view import ThesisSearchView
from common.views.department_list_view import DepartmentListView

urlpatterns = [
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('search-users/', UserSearchView.as_view(), name='search-users'),
    path('search-topics/', ThesisSearchView.as_view(), name='search-topics'),
    path('department/', DepartmentView.as_view(), name='department-view')
]