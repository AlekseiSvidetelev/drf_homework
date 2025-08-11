from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_course_update_information(x, y):
    """ Отправляет письмо с информацией об изменении в курсе """
    return x + y