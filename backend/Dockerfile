FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir \
    django \
    djangorestframework \
    psycopg2-binary \
    pytest \
    pytest-django \
    djangorestframework-simplejwt \
    dj-rest-auth \
    django-environ \
    pyjwt \
    drf-yasg \
    parameterized \
    pytest-cov \
    drf-spectacular \
    django-cors-headers\
    drf-spectacular \
    django-cors-headers\
    drf-spectacular \
    django-filter
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]