import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file)))
sys.path.append(os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = 'caminus.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
