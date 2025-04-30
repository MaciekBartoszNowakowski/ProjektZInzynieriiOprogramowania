from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(
        max_length=100
    )
    description = models.TextField()  
    
    def __str__(self):
        return f'Wydział: {self.name} \nOpis: {self.description}'
    
class Tag(models.Model):
    name = models.CharField(
        max_length=100
    )
    
    def __str__(self):
        return self.name