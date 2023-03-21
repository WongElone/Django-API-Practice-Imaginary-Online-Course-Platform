from django.db import models
from django.conf import settings

# Create your models here.
class CourseCategory(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='courses')

    def __str__(self) -> str:
        return self.title
    
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, blank=True, related_name='teachers')

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, blank=True, related_name='students')

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

class UserRole(models.Model):
    class Role(models.TextChoices):
        TEACHER = 'TE', 'Teacher'
        STUDENT = 'ST', 'Student'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=Role.choices)

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    allow_submit = models.BooleanField(default=True)
    teachers = models.ManyToManyField(Teacher, related_name='assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')

    def __str__(self) -> str:
        return self.title
    
