from django.db import models
from thesis.models import Thesis
from users.models import StudentProfile

class SubmissionStatus(models.TextChoices):
    OPEN = 'aktywne', 'Aktywne'
    ACCEPTED = 'zaakceptowane', 'Zaakceptowane'
    REJECTED = 'odrzucone', 'Odrzucone'


class Submission(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.PROTECT)
    thesis = models.ForeignKey(Thesis, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=50,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.OPEN
    )
