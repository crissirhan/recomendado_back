from recomendado_backend.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['35.196.31.174']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Recomendado-DB-Dev',
        'HOST': '35.185.125.245',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'ckItdb01MZF3'
    }
}
