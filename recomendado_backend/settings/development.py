from recomendado_backend.settings.base import *

DEBUG = True

# Here in the OS the images and files witll be uploaded and served
MEDIA_ROOT = '/var/www/recomendado/'
MEDIA_URL = os.path.join(BASE_DIR,'/media/')
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'recomendado.sqlite'
    }
}
