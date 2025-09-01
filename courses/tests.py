from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson
from users.models import User


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@example.com",
        )
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Description",
            course=self.course,
            owner=self.user,
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )
        self.client.force_authenticate(user=self.user)

    def test_lessons_retrieve(self):
        url = reverse("courses:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("title"),
            self.lesson.title,
        )

    def test_lesson_create(self):
        url = reverse("courses:lesson_create")
        data = {
            "title": "Test Lesson",
            "description": "Test Description",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            2,
        )

    def test_lessons_update(self):
        url = reverse("courses:lesson_update", args=(self.lesson.pk,))
        data = {
            "title": "Test Lesson Update",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("title"),
            "Test Lesson Update",
        )

    def test_lessons_delete(self):
        url = reverse("courses:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            0,
        )

    def test_lessons_list(self):
        url = reverse("courses:lesson_list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": self.lesson.video_url,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview_image": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.json(), result)


class CoursesTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@example.com",
        )
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Description",
            course=self.course,
            owner=self.user,
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("title"),
            self.course.title,
        )

    def test_courses_create(self):
        url = reverse("courses:course-list")
        data = {
            "title": "Test Courses",
            "description": "Test Description Courses",
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Course.objects.all().count(),
            2,
        )

    def test_courses_update(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        data = {
            "title": "Test Course Update",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("title"),
            "Test Course Update",
        )

    def test_lessons_delete(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(
            Course.objects.all().count(),
            0,
        )

    def test_lessons_list(self):
        url = reverse("courses:course-list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
