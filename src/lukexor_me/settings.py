"""
Django settings for lukexor_me project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import sys
from django.conf import global_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['P_SECRET']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

SITE_ID = 1
DOMAIN_NAME = 'lukexor.me'
SITE_NAME = 'lukexor.me'

ALLOWED_HOSTS = [
    u'lukexor.me',
    u'lucaspetherbridge.com',
    u'mindyou.me',
]

AUTH_USER_MODEL = 'lukexor_me.CustomUser'


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'lukexor_me',
    'markdown_deux',
    'honeypot',
    'compressor',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware', # This must be first on the list
    'htmlmin.middleware.HtmlMinifyMiddleware', # After UpdateCacheMiddleware'
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # This must be last
    'htmlmin.middleware.MarkRequestMiddleware', # Actually this comes after FetchFromCacheMiddleware
)

ROOT_URLCONF = 'lukexor_me.urls'
WSGI_APPLICATION = 'lukexor_me.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['LUKEXOR_DB_NAME'],
        'USER': os.environ['LUKEXOR_DB_USER'],
        'PASSWORD': os.environ['LUKEXOR_DB_PASS'],
        'HOST': os.environ['LUKEXOR_DB_HOST'],
        'PORT': os.environ['LUKEXOR_DB_PORT'],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, '../media/')  # Uploaded media files will end up here
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../static/')  # Static files will be collected to here

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),  # This is where static files will be collected from
)
STATICFILES_FINDERS = global_settings.STATICFILES_FINDERS + (
    'compressor.finders.CompressorFinder',
)

COMPRESS_PARSER = 'compressor.parser.BeautifulSoupParser'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# https://docs.djangoproject.com/en/dev/topics/http/sessions/#configuring-sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'localhost:6379:3',
        'KEY_PREFIX': SITE_NAME,
        'OPTIONS': {
            'DB': 3,
            'SOCKET_TIMEOUT': 5,
            'COMPRESS_MIN_LEN': 10,
            "IGNORE_EXCEPTIONS": True,
        },
    },
}
CACHE_TIMES = {
    'labels': 60 * 60 * 24, # 1 day
    # 'post': 60 * 60 * 24 * 7, # 1 week
    'post': 0, # TODO Temp set as 0 until I can figure out how to clear it reliably
    'static': 60 * 60 * 24 * 30, # 1 month
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'lukexor_me.context_processor.GlobalVars',
    'lukexor_me.context_processor.BaseURL',
)

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
            "nofollow": True,
        },
        "safe_mode": "escape",
    },
    "trusted": {
        "extras": {
            "code-friendly": True,
            "markdown-in-html": True,
            "footnotes": True,
        },
        # Allow raw HTML (WARNING: don't use this for user-generated Markdown)
        "safe_mode": False,
    },
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_SSL = False

COMMENTS_ENABLED = True
PAGE_LIMITS = {
    'search': 20,
    'articles': 5,
    'projects': 5,
}
AVG_WPM_READING_SPEED = 120.0

HONEYPOT_FIELD_NAME = 'homepage'
HONEYPOT_VALUE = 'https://'

# Global vars
GA_CODE = '''
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', os.environ['GA_CODE'], 'lukexor.me');
  ga('require', 'linkid', 'linkid.js');
  ga('send', 'pageview');
</script>
'''
URLS = {
    'linkedin': 'https://linkedin.com/in/lucaspetherbridge',
    'github': 'https://github.com/lukexor',
    'gravatar': 'https://gravatar.com/avatar/%s?s=100&amp;r=pg&amp;d=mm',
    'facebook': 'https://www.facebook.com/lukexor',
    'twitter': 'https://twitter.com/lukexor',
    'googleplus': 'https://plus.google.com/+LucasPetherbridge',
    'share_twitter': 'https://twitter.com/intent/tweet?url=%s&amp;text=%s&amp;via=lukexor',
    'share_facebook': 'https://facebook.com/sharer.php?u=%s',
    'share_google': 'https://plus.google.com/share?url=%s',
    'feedburner': 'https://feeds.feedburner.com/LucasPetherbridge',
}
STRINGS = {
    'admin_email': 'Lucas Petherbridge <lukexor@gmail.com>',
    'plain_email': 'lukexor@gmail.com',
    'copyright': 'Copyright (c) - Lucas Petherbridge',
    'full_name': 'Lucas Petherbridge',
    'homepage_description': "My name is Lucas Petherbridge. I'm a programmer and technology enthusiast. I love to code and write articles about topics that intrigue and inspire me.",
    'homepage_keywords': "lucas petherbridge, petherbridge, programming, software development, code",
    'no_reply_email': 'lukexor.me <noreply@lukexor.me>',
    'reverse_email': 'moc.liamg@roxekul',
    'site_subtitle': 'Developer. Technology Enthusiast.',
    'twitter': 'lukexor',
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/../logs/django.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'lukexor_me': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
