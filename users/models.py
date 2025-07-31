from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson


class User(AbstractUser):

    username = None
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя", help_text="Имя")
    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Фамилия",
        help_text="Фамилия",
    )
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите почту")

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    tg_name = models.CharField(
        verbose_name="Ник в телеграм",
        max_length=100,
        blank=True,
        null=True,
        help_text="Укажите ник в телеграме",
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="users/avatars",
        blank=True,
        null=True,
        help_text="Загрузите ваш аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):

    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счёт"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", help_text="Пользователь")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата платежа", help_text="Дата платежа")
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        verbose_name="Оплаченный курс",
        help_text="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.PROTECT,
        verbose_name="Оплаченный урок",
        help_text="Оплаченный урок",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма", help_text="Сумма")
    method = models.CharField(
        max_length=30, choices=PAYMENT_METHODS, verbose_name="Способ оплаты", help_text="Способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]


class Subscription(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", help_text="Пользователь")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", help_text="Курс", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки", help_text="Дата подписки")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
