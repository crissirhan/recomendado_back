## Repositorio para el backend de Recomendado

Proyecto realizado usando Django Rest Framework ( https://www.djangoproject.com/ y http://www.django-rest-framework.org/)
Settings ubicados en recomendado_backend/settings/, configurar ahi la base de datos a utilizar

Branch master actualizada. Último commit estable 1f30916dae6a7696fcbf19b7fe1da8d9dd78f55b

Para echar a correr rápido instalar los paquetes que salen en requirements.txt y hacer runserver . ej: python manage.py runserver --settings=recomendado_backend.settings.local_development

Los servidores de google cloud estaban configurados a partir del boilerplate de Bitnami Django (https://bitnami.com/stack/django), pero usan apache y son comunes y silvestres en todo sentido. Recordar poner en producción usando el wsgi.py (referise a la documentación de django para más información).
