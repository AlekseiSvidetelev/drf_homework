from django.core.management import BaseCommand

from courses.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    """Добавляет платежи в базу данных"""

    help = "Добавляет платежи в базу данных"

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            email="test@test.com", defaults={"password": "123456", "first_name": "test", "last_name": "test"}
        )
        self.stdout.write(self.style.SUCCESS(f'Пользователь "{user.email}" успешно создан'))

        course, _ = Course.objects.get_or_create(title="test_course", defaults={"description": "test_description"})
        self.stdout.write(self.style.SUCCESS(f'Курс "{course.title}" успешно создан'))

        lessons_data = [
            {
                "title": "test_lesson",
                "description": "test_description",
                "video_url": "https://www.test.com/watch?v=123456789",
                "course": course,
            },
            {
                "title": "test_lesson_1",
                "description": "test_description_1",
                "video_url": "https://www.test_1.com/watch?v=123456789",
                "course": course,
            },
            {
                "title": "test_lesson_2",
                "description": "test_description_2",
                "video_url": "https://www.test_2.com/watch?v=123456789",
                "course": course,
            },
        ]

        lesson_objects = []
        for lesson_data in lessons_data:
            lesson, created = Lesson.objects.get_or_create(title=lesson_data["title"], defaults=lesson_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Урок "{lesson.title}" успешно создан'))
            else:
                self.stdout.write(self.style.WARNING(f'Урок "{lesson.title}" уже существует.'))
            lesson_objects.append(lesson)
        payments = [
            {"user": user, "paid_course": course, "paid_lesson": lesson_objects[0], "amount": 1000, "method": "cash"},
            {
                "user": user,
                "paid_course": course,
                "paid_lesson": lesson_objects[1],
                "amount": 2000,
                "method": "transfer",
            },
            {"user": user, "paid_course": course, "paid_lesson": lesson_objects[2], "amount": 3000, "method": "cash"},
        ]

        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(
                user=payment_data["user"],
                paid_course=payment_data["paid_course"],
                paid_lesson=payment_data["paid_lesson"],
                defaults={"amount": payment_data["amount"], "method": payment_data["method"]},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Платеж на сумму {payment.amount} успешно создан"))
            else:
                self.stdout.write(self.style.WARNING(f"Платеж на сумму {payment.amount} уже существует."))
