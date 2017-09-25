from recomendado_backend.settings.base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'recomendado',
        'USER': 'recomendado',
        'PASSWORD': 'recomendado',
        'HOST': 'localhost',
        'PORT': '',
    }
}
