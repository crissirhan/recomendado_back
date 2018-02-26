from recomendado_backend.settings.base import *

DEBUG = True
#MEDIA_ROOT = os.path.join(BASE_DIR,'/images/')# '/home/samir/programacion/recomendado/recomendado_backend/images'
#MEDIA_URL = os.path.join(BASE_DIR,'/media/')

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'recomendado.sqlite'
    }
}
