import os
from datetime import timedelta
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "changeme")

DEBUG = bool(int(os.environ.get("DEBUG", 0)))

ALLOWED_HOSTS: List[str] = []
ALLOWED_HOSTS_ENV = os.environ.get("ALLOWED_HOSTS")
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS.extend(ALLOWED_HOSTS_ENV.split(","))

CSRF_TRUSTED_ORIGINS: List[str] = []
CSRF_TRUSTED_ORIGINS_ENV = os.environ.get("CSRF_TRUSTED_ORIGINS")
if CSRF_TRUSTED_ORIGINS_ENV:
    CSRF_TRUSTED_ORIGINS.extend(CSRF_TRUSTED_ORIGINS_ENV.split(","))

APP_NAME = os.environ.get("APP_NAME")
BUSINESS_PROCESS_HEADER = os.environ.get("BUSINESS_PROCESS_HEADER")
DJANGO_ENV = os.environ.get("DJANGO_ENV")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "api",
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
    "requestlogs.middleware.RequestLogsMiddleware",
    "requestlogs.middleware.RequestIdMiddleware",
    "api.middleware.CustomHeaderMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "api/templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    }
}

LDAP_HOST = os.environ.get("LDAP_HOST", "")
LDAP_PORT = os.environ.get("LDAP_PORT", "")
LDAP_USER_BASEDN = os.environ.get("LDAP_USER_BASEDN", "")
LDAP_USERNAME_FIELD = os.environ.get("LDAP_USERNAME_FIELD", "")
LDAP_APPUSER = os.environ.get("LDAP_APPUSER", "")
LDAP_APPUSER_PASSWORD = os.environ.get("LDAP_APPUSER_PASSWORD", "")

# Authentication
AUTHENTICATION_BACKENDS = [
    "core.auth.backends.LdapAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://:"
        + os.environ.get("CACHE_REDIS_PASSWORD", "")
        + "@"
        + os.environ.get("CACHE_REDIS_HOST", "")
        + ":"
        + os.environ.get("CACHE_REDIS_PORT", ""),
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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    "content-disposition",
    "accept-encoding",
    "content-type",
    "accept",
    "origin",
    "authorization",
    "x-business-process-id",
)

SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "True") == "True"
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "True") == "True"

STATIC_URL = "/static/static/"
STATIC_ROOT = "/vol/web/static"

MEDIA_URL = "/static/media/"
MEDIA_ROOT = "/vol/web/media"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "EXCEPTION_HANDLER": "requestlogs.views.exception_handler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# Logging to Kafka topic
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "")  #
KAFKA_PRODUCER_INIT_RETRIES = int(os.environ.get("KAFKA_PRODUCER_INIT_RETRIES", ""))
KAFKA_FLUSH_BUFFER_SIZE = float(os.environ.get("KAFKA_FLUSH_BUFFER_SIZE", ""))
KAFKA_FLUSH_INTERVAL = float(os.environ.get("KAFKA_FLUSH_INTERVAL", ""))

REQUESTLOGS = {
    "STORAGE_CLASS": "core.logging.storages.MyKafkaStorage",
    "ENTRY_CLASS": "requestlogs.entries.RequestLogEntry",
    "SERIALIZER_CLASS": "requestlogs.storages.RequestIdEntrySerializer",
    "SECRETS": [
        "password",
        "access",
        "token",
        "refresh",
        "HTTP_AUTHORIZATION",
        "HTTP_POSTMAN_TOKEN",
        "email",
        "is_staff",
        "csrfmiddlewaretoken",
        "csrftoken",
        "sessionid",
        "HTTP_COOKIE",
    ],
    "ATTRIBUTE_NAME": "_requestlog",
    "METHODS": ("GET", "PUT", "PATCH", "POST", "DELETE"),
    "JSON_ENSURE_ASCII": True,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "requestlogs_to_kafka": {
            "level": "INFO",
            "class": "core.logging.handlers.MyKafkaLoggingHandler",
        },
    },
    "loggers": {
        "requestlogs": {
            "handlers": ["requestlogs_to_kafka"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
