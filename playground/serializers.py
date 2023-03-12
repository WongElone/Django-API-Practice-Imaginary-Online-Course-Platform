from rest_framework import serializers
from .models import Course, CourseCategory

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'title', 'courses_list', 'slug']

    courses_list = serializers.SerializerMethodField(source='courses', method_name='courses_details')

    def courses_details(self, category):
        courses = Course.objects.filter(category=category)
        return [{
            'id': course.id,
            'title': course.title,
        } for course in courses]

    slug = serializers.SerializerMethodField(method_name='get_slug')

    def get_slug(self, category: CourseCategory):
        return f'{category.id} - {category.title}'
    
class SimpleCourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'title']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'created_at', 'category']

    category = SimpleCourseCategorySerializer()
    
class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'category']
    
    def validate(self, attrs):
        foul_lang = ['fuck', 'ass', 'shit']
        if any(word in attrs['title'] for word in foul_lang) or attrs['title'] == 'fucky':
            return serializers.ValidationError('Title must not contain foul languages')
        return attrs
        