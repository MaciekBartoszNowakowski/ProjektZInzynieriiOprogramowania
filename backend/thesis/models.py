from django.db import models
from django.utils import timezone
from users.models import SupervisorProfile
from common.models import Tag

class ThesisType(models.TextChoices):
    ENGINEERING = 'inżynierska', 'Inżynierska'
    BACHELOR = 'licencjacka', 'Licencjacka'
    MASTER = 'magisterska', 'Magisterska'
    DOCTOR = 'doktorska', 'Doktorska'


class ThesisStatus(models.TextChoices):
    APP_OPEN = 'otwarta', 'Otwarta'
    APP_CLOSED = 'w realizacji', 'W realizacji'
    FINISHED = 'zakończona', 'Zakończona'


class Thesis(models.Model):
    supervisor_id = models.ForeignKey(
        SupervisorProfile, 
        null=True,
        on_delete=models.SET_NULL
    )
    thesis_type = models.CharField(
        null=True, 
        blank=True,
        max_length=50,
        choices=ThesisType.choices
    )
    name = models.CharField(
        max_length=100
    )
    description = models.TextField(
        null=True, 
        blank=True, 
        default=''
    )
    max_students = models.IntegerField(
        default=1
    )
    status = models.CharField(
        null=True, 
        blank=True,
        max_length=50,
        choices=ThesisStatus.choices,
        default=ThesisStatus.APP_OPEN
    )
    updated_at = models.DateTimeField(
        default=timezone.now
    )
    language = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f'Praca {self.thesis_type}, id promotora {self.supervisor_id}'


class ThesisTags(models.Model):
    topic_id = models.ForeignKey(
        Thesis, 
        null=True,
        primary_key=True,
        on_delete=models.SET_NULL
    )
    tag_id = models.ForeignKey(
        Tag, 
        null=True,
        primary_key=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'Id pracy {self.topic_id}, id tagu {self.tag_id}'
