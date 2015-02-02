"""
Django settings for caminus project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g9%*i3)l8)0y#w)vx&#-rn-94i_*o$g&=p-#)1zqqtoe(ln^e2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    #'api',
    'badges',
    'bounty',
    'donate',
    'forums',
    'local',
    'django_messages',
    'minecraft',
    'mptt',
    'notification',
    'petition',
    #'piston',
    'vault',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'caminus.urls'

WSGI_APPLICATION = 'caminus.wsgi.application'

SITE_ID = 1


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


# Templates
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "local.context.random_quote",
    "local.context.login_form",
    "local.context.forum_activity",
    "local.context.donation_info",
    "local.context.notifications",
    "local.context.javascript_uris",
    "minecraft.context.server_info",
    "appversion.context.git_version",
    "appversion.context.server_hostname",
    "django_messages.context_processors.inbox",
    "petition.context.open_petitions",
)


# Auth
LOGIN_REDIRECT_URL = '/'


# Caminus-specific application settings
APPVERSION_GIT_REPO = os.path.sep.join((os.path.dirname(__file__), '.git'))

CAMINUS_MAX_INVITES = 2

CAMINUS_NEWS_FORUM_ID = 1
CAMINUS_USE_BEANSTALKD = False
CAMINUS_BEANSTALKD_HOST = 'localhost'
CAMINUS_BEANSTALKD_PORT = 11300

CAMINUS_BOUNTY_PRICE=250


# Load any site-local overrides, such as camin.us' database settings, etc
try:
    from local_settings import *
except ImportError, e:
    pass

