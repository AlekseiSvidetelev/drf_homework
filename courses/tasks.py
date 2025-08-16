from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from users.models import Subscription


@shared_task
def send_course_update_information(course_id):
    """Отправляет письмо с информацией об изменении в курсе"""
    subscriptions = Subscription.objects.filter(course_id=course_id, is_active=True).select_related("user", "course")

    for subscription in subscriptions:
        subject = f"Обновление курса {subscription.course.title}"
        message = (
            f"Здравствуйте, {subscription.user.first_name}!\n"
            f'Материалы курса "{subscription.course.title}" были обновлены.\n'
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
        )
