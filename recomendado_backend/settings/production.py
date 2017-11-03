from recomendado_backend.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['35.196.132.161', u'api.recomendado-dev.samir.cl', '127.0.0.1',  ]
# Here in the OS the images and files witll be uploaded and served
MEDIA_ROOT = '/var/www/recomendado/'
MEDIA_URL = os.path.join(BASE_DIR,'/media/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'recomendado',
        'HOST': '35.185.125.245',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'ckItdb01MZF3'
    }
}
