from django.urls import path
from .views.thesis_views import ThesisAddView, AvailableThesisView

urlpatterns = [
    path('add/', ThesisAddView.as_view(), name='thesis-add-form'),
    path('available/', AvailableThesisView.as_view(), name='available-theses'),
]