from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson
from users.models import Payment, User


class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@example.com",
        )
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("email"),
            self.user.email,
        )

    def test_users_create(self):
        url = reverse("users:user-list")
        data = {"email": "test8@example.com", "password": "12345678"}
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            User.objects.all().count(),
            2,
        )

    def test_users_update(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {
            "first_name": "Test Name Update",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("first_name"),
            "Test Name Update",
        )

    def test_user_delete(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(
            User.objects.all().count(),
            0,
        )

    def test_user_list(self):
        url = reverse("users:user-list")
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
                    "id": self.user.pk,
                    "email": self.user.email,
                    "first_name": None,
                    "last_name": None,
                    "tg_name": None,
                    "avatar": None,
                }
            ],
        }
        self.assertEqual(response.json(), result)


class PaymentTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@example.com",
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Description",
            course=self.course,
            owner=self.user,
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )
        self.payment = Payment.objects.create(
            user=self.user, amount=1000, method="cash", paid_course=self.course, paid_lesson=self.lesson
        )

    def test_payment_retrieve(self):
        url = reverse("users:payment-detail", args=(self.payment.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("method"),
            self.payment.method,
        )

    def test_payment_create(self):
        url = reverse("users:payment-list")
        data = {
            "user": self.user.pk,
            "amount": 3000,
            "method": "transfer",
            "paid_course": self.course.pk,
            "paid_lesson": self.lesson.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Payment.objects.all().count(),
            2,
        )

    def test_users_update(self):
        url = reverse("users:payment-detail", args=(self.payment.pk,))
        data = {
            "method": "transfer",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("method"),
            "transfer",
        )

    def test_user_delete(self):
        url = reverse("users:payment-detail", args=(self.payment.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(
            Payment.objects.all().count(),
            0,
        )

    def test_user_list(self):
        url = reverse("users:payment-list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@example.com",
        )
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse("users:subscription")
        data = {"course": self.course.pk}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка добавлена"})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка удалена"})
