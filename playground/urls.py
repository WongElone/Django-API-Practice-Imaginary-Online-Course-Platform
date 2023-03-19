from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

routers = DefaultRouter()
routers.register('course_categories', views.CourseCategoryViewSet)
routers.register('courses', views.CourseViewSet)

urlpatterns = [
    path('', include(routers.urls)),
]