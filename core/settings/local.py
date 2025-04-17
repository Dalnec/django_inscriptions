from .base import *
import os

DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS  = [
    'https://*api.tsifactur.com',
    'https://*.tsifactur.com',
    'http://localhost:8000',
]
 
CSRF_TRUSTED_ORIGINS = [
    'https://*api.tsifactur.com',
    'https://*.tsifactur.com',
    'http://localhost:8000',
    'http://*.nuevacreditsac.com',
    'https://*.nuevacreditsac.com',
]

DATABASES = {
    'default': env.db(),
    'externa': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inscripciones_oficial',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join (BASE_DIR / 'staticfiles')
STATICFILES_DIRS = (os.path.join (BASE_DIR / 'static'),)
STATIC_URL = '/static/'


MEDIA_ROOT = BASE_DIR / "media/"
MEDIA_URL = "/media/"