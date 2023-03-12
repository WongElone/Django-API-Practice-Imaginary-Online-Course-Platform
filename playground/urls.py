from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

routers = DefaultRouter()
routers.register('course_categories', views.CourseCategoryViewSet)
routers.register('courses', views.CourseViewSet)

urlpatterns = [
    path('', include(routers.urls)),
]

# urlpatterns = [
#     path('', views.index, name="index"),
#     path('course_categories/', views.CourseCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('course_categories/<pk>', views.CourseCategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
#     path('courses/', views.CourseViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('courses/<pk>', views.CourseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
# ]