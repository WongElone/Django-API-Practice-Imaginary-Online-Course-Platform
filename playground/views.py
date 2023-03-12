from .serializers import CourseCategorySerializer, CourseSerializer, GetCourseSerializer, CreateUpdateCourseCategorySerializer
from django.shortcuts import get_object_or_404
from .models import CourseCategory, Course
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
        if (self.request.method == 'GET'):
            return CourseCategorySerializer
        return CreateUpdateCourseCategorySerializer
    
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related('category').all()

    def get_serializer_class(self):
        if (self.request.method == 'GET'):
            return GetCourseSerializer
        return CourseSerializer

