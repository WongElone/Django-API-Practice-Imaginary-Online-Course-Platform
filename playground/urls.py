from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('course_categories/', views.CourseCategoryList.as_view()),
    path('course_categories/<pk>', views.CourseCategoryDetail.as_view()),
    path('courses/', views.course_list),
    path('courses/<pk>', views.course_detail),
]