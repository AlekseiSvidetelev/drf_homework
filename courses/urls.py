from django.urls import path
from rest_framework.routers import SimpleRouter

from courses.views import (
    CourseViewSet,
    LessonListView,
    LessonDestroyView,
    LessonUpdateView,
    LessonCreateView,
    LessonRetrieveView,
)
from courses.apps import CoursesConfig

app_name = CoursesConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveView.as_view(), name="lesson_retrieve"),
    path("lessons/create/", LessonCreateView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/update/", LessonUpdateView.as_view(), name="lesson_update"),
    path("lessons/<int:pk>/delete/", LessonDestroyView.as_view(), name="lesson_delete"),
]

urlpatterns += router.urls
