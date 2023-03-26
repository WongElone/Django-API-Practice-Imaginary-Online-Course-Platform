from rest_framework import serializers
from rest_framework import status
from .models import Course, CourseCategory, Teacher, Student, Assignment, AssignmentMaterial, Lesson
# FIXME: decouple
from core.models import User
from django.conf import settings

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class SimpleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title']

class RetrieveCourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'title', 'courses']
    
    courses = SimpleCourseSerializer(many=True, read_only=True)
    
class CourseCategorySerializer(serializers.ModelSerializer):
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
        fields = ['id', 'user', 'profile_picture']

    user = SimpleUserSerializer(read_only=True)
    
class SimpleStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'profile_picture']
    
    user = SimpleUserSerializer(read_only=True)

class RetrieveCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'created_at', 'category', 'teachers', 'students']

    category = SimpleCourseCategorySerializer(read_only=True)
    teachers = SimpleTeacherSerializer(many=True, read_only=True)
    students = SimpleStudentSerializer(many=True, read_only=True)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'category']
        # TODO: allow category to be null  

    def validate(self, attrs):
        foul_lang = ['fuck', 'ass', 'shit']
        if any(word in attrs['title'] for word in foul_lang) or attrs['title'] == 'fucky':
            raise serializers.ValidationError('Title must not contain foul languages')
        return super().validate(attrs)

class UpdateTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['courses', 'profile_picture']

class RetrieveTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'courses', 'profile_picture']

    user = SimpleUserSerializer(read_only=True)
    courses = SimpleCourseSerializer(many=True, read_only=True)

class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['courses', 'profile_picture']

class RetrieveStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'courses', 'profile_picture']
    
    user = SimpleUserSerializer(read_only=True)
    courses = RetrieveCourseSerializer(many=True, read_only=True)

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'allow_submit', 'teacher', 'course']

    id = serializers.IntegerField(read_only=True)
    teacher = SimpleTeacherSerializer(read_only=True)
    course = SimpleCourseSerializer(read_only=True)

    def validate(self, attrs): # add attribute in validate function instead of create and update function can reduce codes       
        attrs['course_id'] = self.context['course_pk']

        request = self.context['request']
        teacher = Teacher.objects.filter(user_id=request.user.id).first()
        if teacher:
            attrs['teacher_id'] = teacher.id
        
        return super().validate(attrs)

class AssignmentMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentMaterial
        fields = ['id', 'name', 'file', 'created_at']

    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        attrs['assignment_id'] = self.context['assignment_pk']
        return super().validate(attrs)

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'course', 'video', 'created_at', 'updated_at']

    id = serializers.IntegerField(read_only=True)
    course = SimpleCourseSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        attrs['course_id'] = self.context['course_pk']
        return super().validate(attrs)