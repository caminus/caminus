from django.conf.urls.defaults import patterns, include, url
from piston.resource import Resource
import handlers

whitelistHandler = Resource(handlers.WhitelistHandler)
motdHandler = Resource(handlers.MOTDHandler)

urlpatterns = patterns('api',
    url(r'^validate/(?P<username>.*)$', whitelistHandler),
    url(r'^motd/(?P<username>.*)$', motdHandler),
    url(r'^balance$', Resource(handlers.BalanceHandler))
)
