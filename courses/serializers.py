from rest_framework.fields import SerializerMethodField, URLField
from rest_framework.serializers import CharField, ModelSerializer

from courses.models import Course, Lesson
from courses.validators import url_validator
from users.models import Subscription


class CourseSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, course):
        """Проверка на подписку пользователя на курс"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=course).exists()
        return False

    class Meta:
        model = Course
        fields = ("id", "title", "preview_image", "description", "is_subscribed")


class LessonSerializer(ModelSerializer):
    video_url = URLField(
        validators=[url_validator],
    )

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
