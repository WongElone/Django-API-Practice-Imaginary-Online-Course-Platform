from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('course_categories/', views.CourseCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('course_categories/<pk>', views.CourseCategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('courses/', views.CourseViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('courses/<pk>', views.CourseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]