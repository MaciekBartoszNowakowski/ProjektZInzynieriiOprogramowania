from django.db import models

from thesis.models import Thesis
from users.models import StudentProfile

class Submission(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.PROTECT)
    thesis = models.ForeignKey(Thesis, on_delete=models.PROTECT)