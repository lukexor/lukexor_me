from lukexor_me import settings
import sys
import os

globals().update(vars(sys.modules['lukexor_me.settings']))

DEBUG = True
TEMPLATE_DEBUG = True

WSGI_APPLICATION = 'lukexor_me.wsgi_dev.application'

ALLOWED_HOSTS = [
    'localhost',
]

CACHES = {
    'debug': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

if DEBUG:
    CACHES['default'] = CACHES['debug']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lukexor_me_dev',
        'USER': os.environ['LUKEXOR_DB_USER'],
        'PASSWORD': os.environ['LUKEXOR_DB_PASS'],
        'HOST': os.environ['LUKEXOR_DB_HOST'],
        'PORT': os.environ['LUKEXOR_DB_PORT'],
    }
}

settings.MIDDLEWARE_CLASSES = list(settings.MIDDLEWARE_CLASSES)
settings.MIDDLEWARE_CLASSES.remove('django.middleware.clickjacking.XFrameOptionsMiddleware')
settings.MIDDLEWARE_CLASSES = tuple(settings.MIDDLEWARE_CLASSES)
