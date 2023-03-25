from rest_framework import serializers
from rest_framework import status
from .models import Course, CourseCategory, Teacher, Student, Assignment, Lesson

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
        fields = ['title', 'category']
        # TODO: allow category to be null  

    def validate(self, attrs):
        foul_lang = ['fuck', 'ass', 'shit']
        if any(word in attrs['title'] for word in foul_lang) or attrs['title'] == 'fucky':
            raise serializers.ValidationError('Title must not contain foul languages')
        return super().validate(attrs)


class PutTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['courses']

class GetTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'user_id', 'courses']

    courses = SimpleCourseSerializer(many=True)

class PutStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['courses']

class GetStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user_id', 'courses']
    
    courses = GetCourseSerializer(many=True)

class CustomValidationError(serializers.ValidationError):
    default_code = 'custom_error'
    default_detail = 'Only authorized for admin or teachers of the course'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'allow_submit', 'teacher', 'course']

    id = serializers.IntegerField(read_only=True)
    teacher = SimpleTeacherSerializer(read_only=True)
    course = SimpleCourseSerializer(read_only=True)

    def validate(self, attrs):
        request = self.context['request']
        teacher = Teacher.objects.filter(user_id=request.user.id).prefetch_related('courses').first()
        student = Student.objects.filter(user_id=request.user.id).first()
        course = Course.objects.filter(pk=self.context['course_pk']).first()
        
        if request.user.is_staff or \
        (teacher and course.id in (teacher_course.id for teacher_course in teacher.courses.all())):
            attrs['course_id'] = course.id
            if teacher:
                attrs['teacher_id'] = teacher.id
            return super().validate(attrs)
        raise serializers.ValidationError('Only authorized for admin or teachers of the course')

# class GetAssignmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Assignment
#         fields = ['id', 'title', 'allow_submit', 'teacher', 'course']       

#     teacher = SimpleTeacherSerializer()
#     course = SimpleCourseSerializer()

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'course']

    id = serializers.IntegerField(read_only=True)
    course = SimpleCourseSerializer(read_only=True)

    def validate(self, attrs):
        request = self.context['request']
        teacher = Teacher.objects.filter(user_id=request.user.id).first()
        course = Course.objects.filter(pk=self.context['course_pk']).first()

        if request.user.is_staff or \
        (teacher and teacher.id in (course_teacher.id for course_teacher in course.teachers.all())):
            attrs['course_id'] = self.context['course_pk']
            return super().validate(attrs)
        raise serializers.ValidationError('Only authorized for admin or teachers of the course')