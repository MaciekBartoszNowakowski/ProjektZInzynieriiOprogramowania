from django.db import models

class ThesisType(models.TextChoices):
    ENGINEERING = 'inżynierska', 'Inżynierska'
    BACHELOR = 'licencjacka', 'Licencjacka'
    MASTER = 'magisterska', 'Magisterska'
    DOCTOR = 'doktorska', 'Doktorska'
