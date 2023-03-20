from .serializers import CourseCategorySerializer, CourseSerializer, GetCourseSerializer, CreateUpdateCourseCategorySerializer, TeacherSerializer, GetTeacherSerializer, StudentSerializer, GetStudentSerializer, AssignmentSerializer, GetAssignmentSerializer, PostAssignmentSerializer, MemberSerializer
from django.shortcuts import get_object_or_404
from .models import CourseCategory, Course, Teacher, Student, Assignment, Member
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    
class MemberViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        if request.user.id is None:
            return Response('Need login before viewing your own profile.', status=status.HTTP_401_UNAUTHORIZED)
        (member, created) = Member.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = MemberSerializer(member)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = MemberSerializer(member, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
