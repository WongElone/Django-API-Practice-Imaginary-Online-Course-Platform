from rest_framework import permissions
from .models import Student, Teacher, Course

class IsAdminOrCourseTeacherOrCourseStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        course_pk = view.kwargs['course_pk']
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

class IsAdminOrCourseTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        course_pk = view.kwargs['course_pk']
        course = Course.objects.filter(pk=course_pk).first()
        if not course:
            return True
        
        teacher = Teacher.objects.filter(user_id=request.user.id).prefetch_related('courses').first()
        return bool(teacher and \
                    course.id in (teacher_course.id for teacher_course in teacher.courses.all()))