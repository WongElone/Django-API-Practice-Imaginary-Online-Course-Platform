from rest_framework import serializers
from .models import Course, CourseCategory, Teacher, Student, Assignment

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
        fields = ['id', 'user_id']

class SimpleStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user_id']

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
        fields = ['courses']


class GetTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'user_id', 'courses']

    courses = SimpleCourseSerializer(many=True)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['courses']

class GetStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user_id', 'courses']
    
    courses = GetCourseSerializer(many=True)

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['title', 'allow_submit', 'teachers']
    # should not allow chaning course that the assignment belongs to in PUT and PATCH

    def validate(self, attrs):
        related_teachers = Teacher.objects.filter(
            courses=Assignment.objects.get(
                pk=self.context['assignment_id']
            ).course
        )
        related_teachers_ids = [teacher.id for teacher in related_teachers]
        if not all((teacher.id in related_teachers_ids) for teacher in attrs['teachers']):
        # if any teacher in attr['teachers'] is not related to the course
            raise serializers.ValidationError('Chosen teacher is not in the course')
        return attrs
    
class PostAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['title', 'allow_submit', 'teachers', 'course']

    def validate(self, attrs):
        related_teachers = Teacher.objects.filter(
            courses=self.initial_data['course'][0]
        )
        related_teachers_ids = [teacher.id for teacher in related_teachers]
        if not all((int(teacher_id) in related_teachers_ids) for teacher_id in self.initial_data['teachers']):
            raise serializers.ValidationError('Chosen teacher is not in chosen course')
        return attrs

class GetAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'allow_submit', 'teachers', 'course']

    teachers = SimpleTeacherSerializer(many=True)
    course = SimpleCourseSerializer()

