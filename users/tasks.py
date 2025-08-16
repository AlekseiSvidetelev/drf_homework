from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivated_user_status():
    todey = timezone.now().today()
    one_month_ago = todey - timezone.timedelta(days=5)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    count = inactive_users.update(is_active=False)
    return f"Заблокировано {count} пользователей"
