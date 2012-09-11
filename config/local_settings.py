# Local settings that don't get checked into git.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'caminus',
        'USER': '{{db_user}}',
        'PASSWORD': '{{db_password}}',
        'HOST': '{{db_host}}',
        'PORT': '',
    },
}

TEMPLATE_DIRS = (
    "/usr/share/caminus/templates/"
)

STATIC_URL = "http://caminus-static.s3-website-us-east-1.amazonaws.com"
ADMIN_MEDIA_PREFIX = "http://caminus-static.s3-website-us-east-1.amazonaws.com/admin/"

APPVERSION_GIT_REPO = "/usr/share/caminus/"

CACHES = {
        'default': {
                'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                'LOCATION': 'cache',
        }
}

ADMINS = (
        ('Team Caminus', 'team@camin.us'),
	('Trever Fischer', 'wm161@wm161.net'),
)

MANAGERS = ADMINS

DWOLLA_API_KEY = '{{dwolla_key}}'
DWOLLA_API_SECRET = '{{dwolla_secret}}'
DWOLLA_API_ID = '{{dwolla_id}}'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

CAMINUS_NEWS_FORUM_ID = 10
CAMINUS_DONATION_GOAL = 80

CAMINUS_BEANSTALKD_HOST='queue.camin.us'
CAMINUS_BEANSTALKD_PORT=11300
CAMINUS_USE_BEANSTALKD=False

STRIPE_KEY='{{stripe_key}}
