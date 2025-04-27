from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    STUDENT = 'student', 'Student'
    SUPERVISOR = 'promotor', 'Promotor'
    COORDINATOR = 'koordynator wydziału', 'Koordynator wydziału'
    ADMIN = 'admin', 'Admin'

class AcademicTitle(models.TextChoices):
    NONE = 'brak', 'Brak'
    ENGINEER = 'inżynier', 'Inżynier'
    BACHELOR = 'licencjat', 'Licencjat'
    MASTER = 'magister', 'Magister'
    DOCTOR = 'doktor', 'Doktor'
    HABILITATED_DOCTOR = 'doktor habilitowany', 'Doktor habilitowany'
    PROFESSOR = 'profesor', 'Profesor'
    
class User(AbstractUser):
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.STUDENT
    )
    academic_title = models.CharField(
        max_length=50,
        choices=AcademicTitle.choices,
        default=AcademicTitle.NONE
    )
    description = models.TextField(default="")
    updated_at = models.DateTimeField(("updated_at"), default=timezone.now)