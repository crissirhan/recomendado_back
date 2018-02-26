from recomendado_backend.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['35.198.49.68', u'dev.api.recomendado.cl', '127.0.0.1',  ]
# Here in the OS the images and files witll be uploaded and served
MEDIA_ROOT = '/var/www/recomendado/'
MEDIA_URL = os.path.join(BASE_DIR,'/media/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'recomendado',
        'HOST': '35.199.94.113',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'FbG8lgPKy8lp8x7H'
    }
}
