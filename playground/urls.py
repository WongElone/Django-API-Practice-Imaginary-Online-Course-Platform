from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

routers = DefaultRouter()
routers.register('course_categories', views.CourseCategoryViewSet)
routers.register('courses', views.CourseViewSet)
routers.register('teachers', views.TeacherViewSet)
routers.register('students', views.StudentViewSet)
routers.register('assignments', views.AssignmentViewSet)
routers.register('members', views.MemberViewSet)

urlpatterns = [
    path('', include(routers.urls)),
]