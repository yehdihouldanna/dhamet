"""
WSGI config for DhametFront project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# path = '/home/yehdih/dhamet/dhamet'
# if path not in sys.path:
#     sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DhametFront.settings')

application = get_wsgi_application()
