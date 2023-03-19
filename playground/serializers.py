from rest_framework import serializers
from .models import Course, CourseCategory, Teacher, Student

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'title', 'courses', 'slug']

    courses = serializers.SerializerMethodField(source='courses', method_name='courses_details')

    def courses_details(self, category):
        #FIXME:
        courses = Course.objects.filter(category=category)
        return [{
            'id': course.id,
            'title': course.title,
        } for course in courses]
        

    slug = serializers.SerializerMethodField(method_name='get_slug', read_only=True)

    def get_slug(self, category: CourseCategory):
        return f'{category.id} - {category.title}'
    
class CreateUpdateCourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['title', 'courses']
    
class SimpleCourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'title']

class GetCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'created_at', 'category']

    category = SimpleCourseCategorySerializer()

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'category']

    def validate(self, attrs):
        foul_lang = ['fuck', 'ass', 'shit']
        if any(word in attrs['title'] for word in foul_lang) or attrs['title'] == 'fucky':
            raise serializers.ValidationError('Title must not contain foul languages')
        return attrs


# class TeacherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Teacher
#         fields = ['first_name', 'last_name', 'courses']