from .base import *
import os

DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

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
 
CSRF_TRUSTED_ORIGINS = [
    'https://*api.tsifactur.com',
    'https://*.tsifactur.com',
    'http://localhost:8000',
    'https://*api.tsi.pe',
    'https://*.tsi.pe',
    'http://localhost:5160',
    'http://192.168.0.111:5160',
    'http://localhost:5030',
    'http://192.168.0.111:5030',
]

DATABASES = {
    'default': env.db(),
    'externa': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oldinscriptionsdb', #'inscripciones_oficial',
        'USER': 'postgres',
        'PASSWORD': '07712546150990+', #'admin',
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

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'  # 'mail.tsi.pe'
EMAIL_HOST_USER = env('SMTP_EMAIL')
EMAIL_HOST_PASSWORD = env('SMTP_PASS')
EMAIL_PORT = 587