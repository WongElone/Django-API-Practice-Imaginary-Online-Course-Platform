from .serializers import CourseCategorySerializer, CourseSerializer, CreateCourseSerializer, CreateUpdateCourseCategorySerializer
from django.shortcuts import get_object_or_404
from .models import CourseCategory, Course
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from rest_framework.views import APIView
from pprint import pprint


# Create your views here.
@api_view()
def index(request):
    return Response('ok')

class CourseCategoryList(APIView):
    def get(self, request):
        queryset = CourseCategory.objects.prefetch_related('courses').all()
        serializer = CourseCategorySerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CreateUpdateCourseCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        pprint(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CourseCategoryDetail(APIView):
    def get(self, request, pk):
        category = CourseCategory.objects.get(pk=pk)
        serializer = CourseCategorySerializer(category)
        return Response(serializer.data)
    def put(self, request, pk):
        category = CourseCategory.objects.get(pk=pk)
        serializer = CreateUpdateCourseCategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def patch(self, request, pk):
        category = CourseCategory.objects.get(pk=pk)
        serializer = CreateUpdateCourseCategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view()
def course_category_list(request):
    queryset = CourseCategory.objects.all()
    serializer = CourseCategorySerializer(queryset, many=True)
    pprint(serializer.data)
    return Response(serializer.data)

@api_view()
def course_category_detail(request, pk):
    course_category = get_object_or_404(CourseCategory, pk=pk)
    serializer = CourseCategorySerializer(course_category)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def course_list(request):
    if request.method == 'GET':
        queryset = Course.objects.select_related('category').all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CreateCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    elif request.method in ('PUT', 'PATCH'):
        partialUpdate = (request.method == 'PATCH')
        serializer = CreateCourseSerializer(course, data=request.data, partial=partialUpdate)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method in ('DELETE'):
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)