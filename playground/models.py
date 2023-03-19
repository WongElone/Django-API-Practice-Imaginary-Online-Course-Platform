from django.db import models

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
    teachers = models.ManyToManyField(Teacher)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title