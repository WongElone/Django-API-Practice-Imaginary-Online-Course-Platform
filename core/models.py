from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        STUDENT = settings.USER_ROLE_STUDENT, 'Student'
        TEACHER = settings.USER_ROLE_TEACHER, 'Teacher'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=2, choices=RoleChoices.choices, default='ST')
