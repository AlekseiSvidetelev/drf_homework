from rest_framework.serializers import ValidationError


def url_validator(value: str) -> None:
    """Проверка URL на валидность"""
    if "://" not in value:
        raise ValidationError("Неверный формат ссылки")
    after_protocol = value.split("://")[1]
    if after_protocol[:15].lower() != "www.youtube.com":
        raise ValidationError("Можно загрузить только видео с youtube.com")


if __name__ == "__main__":
    url_validator("https://www.youtube.com/watch?v=9bZkp7q19f0")
    url_validator("http://www.youtube.com/watch?v=9bZkp7q19f0")
    url_validator("https://www.rutube.com/watch?v=9bZkp7q19f0")
