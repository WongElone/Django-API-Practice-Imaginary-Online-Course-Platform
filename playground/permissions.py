from rest_framework import permissions
from .models import Student, Teacher, Course
from django.conf import settings

class IsAdminOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff or \
                    (request.user.role == settings.USER_ROLE_TEACHER))

# is admin or teacher of this course or student of this course
class IsAdminOrCourseTeacherOrCourseStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if '/courses/' not in request.path:
            raise Exception('Improper usage of IsAdminOrCourseTeacher permission class')

        if request.user.is_staff:
            return True

        course_pk = view.kwargs.get('course_pk', None) or view.kwargs['pk']
        course = Course.objects.filter(pk=course_pk).first()
        if not course:
            return True # no need to return False, just pass True, cuz django rest framework knows this course doesn't exist anyway
                
        teacher = Teacher.objects.filter(user_id=request.user.id).first()
        if teacher:
            if course.id in (teacher_course.id for teacher_course in teacher.courses.all()):
                return True
            return False
        
        student = Student.objects.filter(user_id=request.user.id).first()
        return bool(student and \
                    course.id in (student_course.id for student_course in student.courses.all()))

# is admin or teacher of this course
class IsAdminOrCourseTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if '/courses/' not in request.path:
            raise Exception('Improper usage of IsAdminOrCourseTeacher permission class')

        if request.user.is_staff:
            return True

        course_pk = view.kwargs.get('course_pk', None) or view.kwargs['pk']
        course = Course.objects.filter(pk=course_pk).first()
        if not course:
            return True
        
        teacher = Teacher.objects.filter(user_id=request.user.id).prefetch_related('courses').first()
        return bool(teacher and \
                    course.id in (teacher_course.id for teacher_course in teacher.courses.all()))