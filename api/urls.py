from django.conf.urls.defaults import patterns, include, url
from piston.resource import Resource
import handlers

whitelistHandler = Resource(handlers.WhitelistHandler)

urlpatterns = patterns('api',
    url(r'^validate/(?P<username>.*)$', whitelistHandler)
)
