from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from common.models import Department, Tag

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
    
ACADEMIC_TITLE_SORT_ORDER = {
    AcademicTitle.NONE: 0,
    AcademicTitle.ENGINEER: 1,
    AcademicTitle.BACHELOR: 2,
    AcademicTitle.MASTER: 3,
    AcademicTitle.DOCTOR: 4,
    AcademicTitle.HABILITATED_DOCTOR: 5,
    AcademicTitle.PROFESSOR: 6,
}
    
class User(AbstractUser):
    role = models.CharField(
        null=True, 
        blank=True,
        max_length=50,
        choices=Role.choices,
        default=Role.STUDENT
    )
    academic_title = models.CharField(
        null=True, 
        blank=True,
        max_length=50,
        choices=AcademicTitle.choices,
        default=AcademicTitle.NONE
    )
    description = models.TextField(
        null=True, 
        blank=True, 
        default=''
    )
    updated_at = models.DateTimeField(
        default=timezone.now
    )
    department = models.ForeignKey(
        Department, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='users'
    )
    
    def __str__(self):
        try:
            title = self.academic_title + ' ' if self.academic_title is not AcademicTitle.NONE else ''
            return f'Profil użytkownika: {title}{self.first_name} {self.last_name}'
        except User.DoesNotExist:
            return 'Profil usuniętego użytkownika'
        
class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,                  
        on_delete=models.CASCADE, 
        primary_key=True
    )
    index_number = models.CharField(
        max_length=6,
        unique=True
    )
    
    def __str__(self):
        try:
            return f'Profil studenta: {self.user.username} ({self.index_number})'
        except User.DoesNotExist:
            return f'Profil studenta dla usuniętego użytkownika ({self.index_number})'
         

class SupervisorProfile(models.Model):
    user = models.OneToOneField(
        User,                  
        on_delete=models.CASCADE, 
        primary_key=True
    )
    bacherol_limit = models.IntegerField(
        default=1
    )
    engineering_limit = models.IntegerField(
        default=1
    )
    master_limit = models.IntegerField(
        default=1
    )
    phd_limit = models.IntegerField(
        default=1
    )
    
    def __str__(self):
        try:
            return f'{self.user.academic_title} {self.user.username}'
        except User.DoesNotExist:
            return 'Profil promotora dla usuniętego użytkownika'

class Logs(models.Model):
    user_id = models.ForeignKey(
        User, 
        null=True,
        on_delete=models.SET_NULL
    )
    description = models.TextField(
        null=True, 
        blank=True, 
        default=''
    )
    timestamp = models.DateTimeField(
        default=timezone.now
    )
    
    def __str__(self):
        user_representation = self.user_id.username if self.user_id else 'Brak użytkownika'
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        desc_snippet = self.description[:50] + '...' if self.description and len(str(self.description)) > 50 else self.description or ''
        return f"Zmiana {self.id} ({timestamp_str}) zrobiona przez {user_representation}: {desc_snippet}"