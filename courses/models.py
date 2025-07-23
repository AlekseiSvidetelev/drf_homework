from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название курса", help_text="Введите название курса")
    preview_image = models.ImageField(upload_to="course_images/", verbose_name="Картинка курса", blank=True, null=True)
    description = models.TextField(verbose_name="Описание курса", help_text="Введите описание курса")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название урока", help_text="Введите название урока")
    description = models.TextField(verbose_name="Описание урока", help_text="Введите описание урока")
    preview_image = models.ImageField(upload_to="lesson_images/", verbose_name="Картинка урока", blank=True, null=True)
    video_url = models.URLField(verbose_name="Ссылка на видео", help_text="Введите ссылку на видео")

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
