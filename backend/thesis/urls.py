from django.urls import path
from .views.thesis_views import ThesisAddView, AvailableThesisView, ThesisUpdateView, ThesisDeleteView, SupervisorThesisView

urlpatterns = [
    path('add/', ThesisAddView.as_view(), name='thesis-add-form'),
    path('update/<int:pk>/', ThesisUpdateView.as_view(), name='update-thesis'),
    path('available/', AvailableThesisView.as_view({'get': 'list'}), name='available-theses'),
    path('available/<int:pk>/', AvailableThesisView.as_view({'get': 'retrieve'}), name='available-theses-detail'),
    path('delete/<int:pk>/', ThesisDeleteView.as_view(), name='delete-thesis'),
    path('my-topics/', SupervisorThesisView.as_view(), name='supervisor-thesis')
]