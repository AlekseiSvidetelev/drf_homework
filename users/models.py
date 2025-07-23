from django.contrib.auth.models import AbstractUser
from django.db import models


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
