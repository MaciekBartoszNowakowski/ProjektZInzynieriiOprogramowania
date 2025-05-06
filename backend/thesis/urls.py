from django.urls import path
from views import ThesisAddView, ThesisStatusView

urlpatterns = [
    path('add/', ThesisAddView.as_view(), name='thesis-form'),
    path('theses/', ThesisStatusView.as_view(), name='present-theses'),
]