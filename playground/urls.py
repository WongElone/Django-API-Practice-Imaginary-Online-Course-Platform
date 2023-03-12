from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('course_categories/', views.course_category_list),
    path('course_categories/<pk>', views.course_category_detail),
    path('courses/', views.course_list),
    path('courses/<pk>', views.course_detail),
]