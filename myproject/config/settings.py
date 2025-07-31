import os
from datetime import timedelta
from pathlib import Path
from celery.schedules import crontab

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",  # администрирование данных в Django-приложениях
    "django.contrib.auth",  # система аутентификации и авторизации пользователей
    "django.contrib.contenttypes",  # инфраструктура для работы с типами моделей, зарегистрированными в проекте
    "django.contrib.sessions", # часть фреймворка, для обеспечения поддержки сессий для веб-приложений
    "django.contrib.messages",  # встроенный фреймворк сообщений, для отображения сообщения пользователям
    "django.contrib.staticfiles",  # встроенное приложение, для управления и обслуживания статических файлов
    "django_extensions",  # дополнительные команды и утилиты для фреймворка Django
    "django_celery_beat",  # расширение, позволяющее хранить расписание периодических задач в бд

    "rest_framework",  # подключаем DRF
    "corsheaders",  # механизм безопасности, используемый браузерами для контроля доступа к ресурсам
    "djoser",  # готовые представления для обработки основных операций аутентификации и авторизации

    # установленные приложения:
    "users",  # приложение для взаимодействия с пользователем
    "habit_tracker", # приложение трекер привычек
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# использование кастомной модели пользователя для авторизации
AUTH_USER_MODEL = "users.CustomUser"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Настройки почты (для отправки писем)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.rambler.ru"  # используемый SMTP сервер
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# Используем Redis в качестве кеша
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",  # правильный путь для django-redis
        "LOCATION": "redis://127.0.0.1:6379/1",  # расположение Redis-сервера
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Настройки JWT-токенов
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",  # по умолчанию все защищены
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 5,
}

# Настройки срока действия токенов
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# Конфигурация для Swagger (инструмента для документирования и тестирования
# REST API), которая определяет способы аутентификации, используемые в нашем API.
SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {  # словарь, где описываются методы безопасности (аутентификации)
      'Basic': {  # базовая аутентификация HTTP (клиент отправляет логин и пароль в заголовке запроса)
            'type': 'basic'
      },
      'Bearer': {  # аутентификация по токену (у нас JWT), где токен передается в заголовке Authorization
            'type': 'apiKey',  # аутентификация происходит через API-ключ.
            'name': 'Authorization',  # имя HTTP-заголовка, в котором передается токен
            'in': 'header'  # указывает, что ключ (токен) передается в заголовке запроса
      }
   }
}

# Настройки для Celery

# URL-адрес брокера сообщений (Redis по умолчанию работает на порту 6379)
CELERY_BROKER_URL = os.getenv('REDIS_URL')

# URL-адрес брокера результатов, также Redis
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

# Часовой пояс для работы Celery
CELERY_TIMEZONE = "UTC"

# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True

# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {
    'deactivate_inactive_users_every_day': {
    'task': 'users.tasks.deactivate_inactive_users',
    'schedule': crontab(hour=0, minute=0),  # каждый день в 00:00
    },
}

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = int(os.getenv('TELEGRAM_CHAT_ID'))
