from .serializers import CourseCategorySerializer, CourseSerializer, GetCourseSerializer, CreateUpdateCourseCategorySerializer, PutTeacherSerializer, GetTeacherSerializer, PutStudentSerializer, GetStudentSerializer, AssignmentSerializer, LessonSerializer
from django.shortcuts import get_object_or_404
from .models import CourseCategory, Course, Teacher, Student, Assignment, Lesson
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, SAFE_METHODS
from rest_framework import serializers
from django.db import transaction
from .permissions import IsAdminOrCourseTeacher, IsAdminOrCourseTeacherOrCourseStudent
    
class CourseCategoryViewSet(ModelViewSet):
    queryset = CourseCategory.objects.prefetch_related('courses').all()
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseCategorySerializer
        return CreateUpdateCourseCategorySerializer
        # request.data.course in [course.id for course in teacher.courses]

class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.select_related('user').prefetch_related('courses').all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTeacherSerializer
        return PutTeacherSerializer
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        teacher = Teacher.objects.get(user_id=request.user.id)
        if teacher is None:
            return Response('your account is not a teacher account', status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == 'GET':
            serializer = GetTeacherSerializer(teacher)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = PutTeacherSerializer(teacher, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.select_related('user').prefetch_related('courses').all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetStudentSerializer
        return PutStudentSerializer
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        student = Student.objects.get(user_id=request.user.id)
        if student is None:
            return Response('your account is not a student account', status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            serializer = GetStudentSerializer(student)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = PutStudentSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class CourseViewSet(ModelViewSet):
    def get_queryset(self):
        return Course.objects.select_related('category').prefetch_related('teachers', 'students').all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        elif self.request.method in ('PUT', 'POST'):
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetCourseSerializer
        return CourseSerializer
        # TODO: for PUT, only the course teacher and admin can change course detail

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id
        return context
    
    def create(self, request, *args, **kwargs):
        teacher = Teacher.objects.filter(user_id=self.request.user.id).first()
        self.request.user.teacher = teacher
        if self.request.user.is_staff or self.request.user.teacher:
            return super().create(request, *args, **kwargs)
        return Response('Require admin or teacher account.', status=status.HTTP_403_FORBIDDEN)
        # TODO: multiple teacher course

    def perform_create(self, serializer):
        teacher = self.request.user.teacher       
        # if self.request.user.is_staff or teacher:
        with transaction.atomic():
            newCourse = serializer.save()
            # if user is teacher, add course to the teacher
            if teacher:
                teacher.courses.add(newCourse)
                teacher.save()

class AssignmentViewSet(ModelViewSet):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated(), IsAdminOrCourseTeacherOrCourseStudent()]
        return [IsAuthenticated(), IsAdminOrCourseTeacher()]

    def get_queryset(self):
        return Assignment.objects.filter(
            course_id=self.kwargs['course_pk']
            ).select_related('course', 'teacher').all()

    def get_serializer_context(self):
        # by calling super().get_serializer_context(), request will be passed to serializer context
        context = super().get_serializer_context()
        context['course_pk'] = self.kwargs['course_pk']
        return context

    def get_serializer_class(self):
        return AssignmentSerializer

class LessonViewSet(ModelViewSet):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated(), IsAdminOrCourseTeacherOrCourseStudent()]
        return [IsAuthenticated(), IsAdminOrCourseTeacher()]

    def get_queryset(self):
        return Lesson.objects.filter(
            course_id=self.kwargs['course_pk']
            ).select_related('course').all()

    def get_serializer_class(self):
        return LessonSerializer
    
    def get_serializer_context(self):
        # by calling super().get_serializer_context(), request will be passed to serializer context
        context = super().get_serializer_context()
        context['course_pk'] = self.kwargs['course_pk']
        return context