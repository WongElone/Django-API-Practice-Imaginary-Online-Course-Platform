from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

# routers = DefaultRouter()
router = routers.DefaultRouter()
router.register(r'course_categories', views.CourseCategoryViewSet)
router.register(r'courses', views.CourseViewSet, basename='Course')
router.register(r'teachers', views.TeacherViewSet)
router.register(r'students', views.StudentViewSet)
# router.register(r'assignments', views.AssignmentViewSet)

courses_router = routers.NestedDefaultRouter(router, r'courses', lookup='course')
courses_router.register(r'assignments', views.AssignmentViewSet, basename='course-assignments')
courses_router.register(r'lessons', views.LessonViewSet, basename='course-lessons')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(courses_router.urls)),
]