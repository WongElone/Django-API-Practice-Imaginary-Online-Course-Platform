from .serializers import CourseCategorySerializer, CourseSerializer, GetCourseSerializer, CreateUpdateCourseCategorySerializer, TeacherSerializer, GetTeacherSerializer, StudentSerializer, GetStudentSerializer, AssignmentSerializer, GetAssignmentSerializer, PostAssignmentSerializer
from django.shortcuts import get_object_or_404
from .models import CourseCategory, Course, Teacher, Student, Assignment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
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
    queryset = Teacher.objects.prefetch_related('courses').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTeacherSerializer
        return TeacherSerializer
    
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.prefetch_related('courses').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetStudentSerializer
        return StudentSerializer

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