from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        STUDENT = 'ST', 'Student'
        TEACHER = 'TE', 'Teacher'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=2, choices=RoleChoices.choices, default='ST')
