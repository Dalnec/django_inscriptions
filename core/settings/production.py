from .base import *

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = [
    host.strip()
    for host in env("DJANGO_ALLOWED_HOSTS", default="jnicampapi.tsi.pe").split(",")
    if host.strip()
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

CORS_ALLOW_ALL_ORIGINS = env.bool("DJANGO_CORS_ALLOW_ALL_ORIGINS", default=False)
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in env(
        "DJANGO_CORS_ALLOWED_ORIGINS",
        default="https://jnicamp.tsi.pe,https://jnicampapi.tsi.pe",
    ).split(",")
    if origin.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in env(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        default="https://jnicampapi.tsi.pe,https://jnicamp.tsi.pe",
    ).split(",")
    if origin.strip()
]

DATABASES = {
    "default": env.db(),
    "externa": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("EXTERNA_DB_NAME", default="oldinscriptionsdb"),
        "USER": env("EXTERNA_DB_USER", default="postgres"),
        "PASSWORD": env("EXTERNA_DB_PASSWORD", default="admin"),
        "HOST": env("EXTERNA_DB_HOST", default="localhost"),
        "PORT": env("EXTERNA_DB_PORT", default="5432"),
    },
}

STATIC_ROOT = "/app/staticfiles"
STATICFILES_DIRS = ()
STATIC_URL = "/static/"

MEDIA_ROOT = "/app/media"
MEDIA_URL = "/media/"

EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = env("SMTP_EMAIL")
EMAIL_HOST_PASSWORD = env("SMTP_PASS")
EMAIL_PORT = 587
