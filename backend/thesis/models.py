from django.db import models
from django.utils import timezone
from users.models import SupervisorProfile
from common.models import Tag

class ThesisType(models.TextChoices):
    ENGINEERING = 'inżynierska', 'Inżynierska'
    BACHELOR = 'licencjacka', 'Licencjacka'
    MASTER = 'magisterska', 'Magisterska'
    DOCTOR = 'doktorska', 'Doktorska'


THESIS_TYPE_SORT_ORDER = {
    ThesisType.ENGINEERING: 1,
    ThesisType.BACHELOR: 1,
    ThesisType.MASTER: 2,
    ThesisType.DOCTOR: 3,
}


class ThesisStatus(models.TextChoices):
    APP_OPEN = 'otwarta', 'Otwarta'
    APP_CLOSED = 'w realizacji', 'W realizacji'
    FINISHED = 'zakończona', 'Zakończona'


class Thesis(models.Model):
    supervisor_id = models.ForeignKey(
        SupervisorProfile,
        on_delete=models.CASCADE
    )
    thesis_type = models.CharField(
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
        max_length=50,
        choices=ThesisStatus.choices,
        default=ThesisStatus.APP_OPEN
    )
    updated_at = models.DateTimeField(
        default=timezone.now
    )
    language = models.CharField(
        null=True, 
        blank=True,
        max_length=100,
        default="English"
    )

    def __str__(self):
        return f'Praca {self.thesis_type}, promotor: {self.supervisor_id}'


class ThesisTags(models.Model):
    topic = models.ForeignKey(
        Thesis,
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag, 
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('topic', 'tag')

    def __str__(self):
        return f'Praca {self.topic.id}, Tag {self.tag.id}'
