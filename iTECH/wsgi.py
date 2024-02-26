"""
<<<<<<<< HEAD:tango_with_django_project/tango_with_django_project/wsgi.py
WSGI config for tango_with_django_project project.
========
WSGI config for iTECH project.
>>>>>>>> a7c67f6 (initial commit):iTECH/wsgi.py

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<<< HEAD:tango_with_django_project/tango_with_django_project/wsgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
========
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iTECH.settings')
>>>>>>>> a7c67f6 (initial commit):iTECH/wsgi.py

application = get_wsgi_application()
