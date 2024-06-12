"""
WSGI config for orders_djg project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.flushdb()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders_djg.settings')

application = get_wsgi_application()
