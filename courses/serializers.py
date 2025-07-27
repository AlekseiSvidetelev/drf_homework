from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from courses.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = SerializerMethodField()

    def get_count_lessons(self, course):
        """Получаем количество уроков у курса"""
        return Lesson.objects.filter(course=course).count()

    def get_lessons(self, course):
        """Получаем уроки у курса"""
        queryset = Lesson.objects.filter(course=course)
        return LessonSerializer(queryset, many=True).data

    class Meta:
        model = Course
        fields = ("id", "title", "description", "count_lessons", "lessons")
