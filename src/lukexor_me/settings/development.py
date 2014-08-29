"""
Django settings for lukexor_me project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from lukexor_me.settings.production import *

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
	'localhost'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'tmp/db.sqlite3'),
    }
}

STATIC_ROOT = '../static/' # Static files will be collected to here
MEDIA_ROOT = '../media/' # Uploaded media files will end up here
