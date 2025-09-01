FROM python:3.13-slim

WORKDIR /code

RUN pip install poetry

COPY README.md /code/README.md
COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi  --no-root

RUN mkdir -p /app/media

COPY . .

EXPOSE 8000


CMD ["sh", "-c", "python manage.py collectstatic --noinput && g"]
