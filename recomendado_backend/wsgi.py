"""
WSGI config for recomendado_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/opt/bitnami/apps/django/django_projects/recomendado_backend')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/recomendado_backend/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recomendado_backend.settings.production")

application = get_wsgi_application()
