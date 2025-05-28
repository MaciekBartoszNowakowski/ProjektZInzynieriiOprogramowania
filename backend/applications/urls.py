from django.urls import path

from applications.views.accept_submission_view import AcceptSubmissionView
from applications.views.cancel_submission import CancelSubmissionView
from applications.views.reject_submission_view import RejectSubmissionView
from applications.views.remove_student_view import RemoveStudentFromThesisView
from applications.views.student_submission_status_view import StudentSubmissionStatusView
from applications.views.submit_to_thesis import SubmitToThesisView
from applications.views.thesis_submission_view import ThesisSubmissionsView
    
urlpatterns = [
    path('submit/', SubmitToThesisView.as_view(), name='submit_to_thesis'),
    path('cancel/', CancelSubmissionView.as_view(), name='cancel_submission'),
    path('status/', StudentSubmissionStatusView.as_view(), name='student_submission_status'),
    path('thesis/<int:thesis_id>/submissions/', ThesisSubmissionsView.as_view(), name='thesis_submissions'),
    path('submissions/<int:submission_id>/accept/', AcceptSubmissionView.as_view(), name='accept_submission'),
    path('submissions/<int:submission_id>/reject/', RejectSubmissionView.as_view(), name='reject_submission'),
    path('submissions/<int:submission_id>/remove/', RemoveStudentFromThesisView.as_view(), name='remove_student'),
]