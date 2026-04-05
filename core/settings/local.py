from .base import *
import os

DEBUG = env("DEBUG")

ALLOWED_HOSTS = [host.strip() for host in env("DJANGO_ALLOWED_HOSTS", default="jnicampapi.tsi.pe").split(",") if host.strip()]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS  = [
#     'https://*api.tsifactur.com',
#     'https://*.tsifactur.com',
#     'https://*api.tsi.pe',
#     'https://*.tsi.pe',
#     'http://localhost:8000',
#     'http://localhost:5160',
#     'http://192.168.0.111:5160',
# ]
 
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in env(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default="https://jnicampapi.tsi.pe,https://jnicamp.tsi.pe",
).split(",") if origin.strip()]

DATABASES = {
    'default': env.db(),
    'externa': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("EXTERNA_DB_NAME", default="oldinscriptionsdb"), #'inscripciones_oficial',
        'USER': env("EXTERNA_DB_USER", default="postgres"),
        'PASSWORD': env("EXTERNA_DB_PASSWORD", default="admin"), #'admin',
        'HOST': env("EXTERNA_DB_HOST", default="localhost"),
        'PORT': env("EXTERNA_DB_PORT", default="5432"),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join (BASE_DIR / 'staticfiles')
STATIC_SOURCE_DIR = BASE_DIR / "static"
STATICFILES_DIRS = [str(STATIC_SOURCE_DIR)] if STATIC_SOURCE_DIR.exists() else []
STATIC_URL = '/static/'


MEDIA_ROOT = BASE_DIR / "media/"
MEDIA_URL = "/media/"

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'  # 'mail.tsi.pe'
EMAIL_HOST_USER = env('SMTP_EMAIL')
EMAIL_HOST_PASSWORD = env('SMTP_PASS')
EMAIL_PORT = 587
