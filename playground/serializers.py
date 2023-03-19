from rest_framework import serializers
from .models import Course, CourseCategory, Teacher, Student


class SimpleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title']
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'title', 'courses', 'slug']
    
    courses = SimpleCourseSerializer(many=True)

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

class SimpleTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name']

class SimpleStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name']

class GetCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'created_at', 'category', 'teachers', 'students']

    category = SimpleCourseCategorySerializer()
    teachers = SimpleTeacherSerializer(many=True)
    students = SimpleStudentSerializer(many=True)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'category', 'teachers']

    def validate(self, attrs):
        foul_lang = ['fuck', 'ass', 'shit']
        if any(word in attrs['title'] for word in foul_lang) or attrs['title'] == 'fucky':
            raise serializers.ValidationError('Title must not contain foul languages')
        return attrs


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'courses']


class GetTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'courses']

    courses = SimpleCourseSerializer(many=True)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'courses']

class GetStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'courses']

    courses = GetCourseSerializer(many=True)