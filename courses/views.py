from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Lesson
from courses.paginators import CustomPageNumberPagination
from courses.serializers import CourseDetailSerializer, CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description=(
            "Удаление курса по идентификатору. "
            "Требует прав администратора или пользователя.\n\n"
            "**Параметры пути:**\n"
            "- `id` (int): Идентификатор курса\n\n"
            "**Ответы:**\n"
            "- `HTTP 204 No Content`: Успешное удаление\n"
            "- `HTTP 404 Not Found`: Курс не найден\n"
            "- `HTTP 403 Forbidden`: Нет прав для удаления\n\n"
        ),
        operation_summary="lessons_delete",
        responses={
            204: "Курс успешно удалён",
            403: "Доступ запрещён",
            404: "Курс не найден",
        },
    ),
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [
                IsModerator | IsOwner,
            ]
        elif self.action == "destroy":
            self.permission_classes = (~IsModerator | IsOwner,)
        elif self.action == "list":
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["lessons"],
        operation_summary="lessons_create",
    ),
)
class LessonCreateView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["lessons"],
        operation_summary="lessons_list",
    ),
)
class LessonListView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPageNumberPagination


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["lessons"],
        operation_summary="lessons_read",
    ),
)
class LessonRetrieveView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )

    def get_serializer_context(self):
        """Добавляем текущий запрос в контекст сериализатора."""
        return {"request": self.request}


@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        tags=["lessons"],
        operation_summary="lessons_update",
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        tags=["lessons"],
        operation_summary="lessons_update_partial",
    ),
)
class LessonUpdateView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_description=(
            "Удаление урока по идентификатору. "
            "Требует прав администратора или пользователя.\n\n"
            "**Параметры пути:**\n"
            "- `id` (int): Идентификатор урока\n\n"
            "**Ответы:**\n"
            "- `HTTP 204 No Content`: Успешное удаление\n"
            "- `HTTP 404 Not Found`: Урок не найден\n"
            "- `HTTP 403 Forbidden`: Нет прав для удаления\n\n"
        ),
        tags=["lessons"],
        operation_summary="lessons_delete",
        responses={
            204: "Урок успешно удалён",
            403: "Доступ запрещён",
            404: "Урок не найден",
        },
    ),
)
class LessonDestroyView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        ~IsModerator | IsOwner,
    )
