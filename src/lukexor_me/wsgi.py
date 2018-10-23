"""
WSGI config for lukexor_me project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import re
from django.core.wsgi import get_wsgi_application

def read_env():
    """Pulled from Honcho code with minor updates, reads local default
    environment variables from a .env file located in the project root
    directory.
    """
    try:
        with open('/home/caeledh/www/lukexor.me/public_html/.env') as f:
            content = f.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)

sys.path.append('/home/caeledh/www/lukexor.me/public_html/src/')
sys.path.append('/home/caeledh/www/lukexor.me/public_html/src/lukexor_me')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lukexor_me.settings")
read_env()
application = get_wsgi_application()
