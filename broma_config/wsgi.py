import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "broma_config.settings.local")
"""
Sets the default Django settings module for the project and initializes the WSGI application.
"""

application = get_wsgi_application()
