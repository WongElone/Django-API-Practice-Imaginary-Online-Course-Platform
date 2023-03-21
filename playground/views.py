from .serializers import CourseCategorySerializer, CourseSerializer, GetCourseSerializer, CreateUpdateCourseCategorySerializer, TeacherSerializer, GetTeacherSerializer, StudentSerializer, GetStudentSerializer, AssignmentSerializer, GetAssignmentSerializer, PostAssignmentSerializer
from django.shortcuts import get_object_or_404
from .models import CourseCategory, Course, Teacher, Student, Assignment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from pprint import pprint


# Create your views here.
@api_view()
def index(request):
    return Response('ok')
    
class CourseCategoryViewSet(ModelViewSet):
    queryset = CourseCategory.objects.prefetch_related('courses').all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseCategorySerializer
        return CreateUpdateCourseCategorySerializer
    
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related('category').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetCourseSerializer
        return CourseSerializer

class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.select_related('user').prefetch_related('courses').all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTeacherSerializer
        return TeacherSerializer
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        teacher = Teacher.objects.get(user_id=request.user.id)
        if teacher is None:
            return Response('your account is not a teacher account', status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == 'GET':
            serializer = GetTeacherSerializer(teacher)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = TeacherSerializer(teacher, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.select_related('user').prefetch_related('courses').all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetStudentSerializer
        return StudentSerializer
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        student = Student.objects.get(user_id=request.user.id)
        if student is None:
            return Response('your account is not a student account', status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            serializer = GetStudentSerializer(student)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = StudentSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.select_related('course').prefetch_related('teachers').all()

    def get_serializer_context(self):
        context = {}
        if 'pk' in self.kwargs:
            context['assignment_id'] = self.kwargs['pk']
        return context

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetAssignmentSerializer
        elif self.request.method == 'POST':
            return PostAssignmentSerializer
        return AssignmentSerializer
    

