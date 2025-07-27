from django.contrib import admin

from courses.models import Course, Lesson


@admin.register(Course)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "preview_image",
        "description",
        "owner",
    )


@admin.register(Lesson)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "preview_image",
        "description",
        "video_url",
        "course",
        "owner",
    )
