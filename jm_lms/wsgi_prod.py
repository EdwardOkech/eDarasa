"""
WSGI config for JMLMS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

sys.path = ['/home/fraogongi/webapps/workstry_app/workstry_project/jmlms/jmlms', 
            '/home/fraogongi/webapps/workstry_app/venv/lib/python2.7'] + sys.path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'jm_lms.settings.prod')

application = get_wsgi_application()

