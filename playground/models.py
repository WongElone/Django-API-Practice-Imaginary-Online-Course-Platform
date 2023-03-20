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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course, blank=True, related_name='teachers')

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course, blank=True, related_name='students')

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    allow_submit = models.BooleanField(default=True)
    teachers = models.ManyToManyField(Teacher, related_name='assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')

    def __str__(self) -> str:
        return self.title
    
class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255)