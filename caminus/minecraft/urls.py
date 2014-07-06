from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('minecraft',
    url(r'^avatar/(?P<size>[0-9]+)/(?P<username>.*).png$', 'views.avatar'),
    url(r'^avatar/(?P<username>.*).png$', 'views.avatar'),
    url(r'^rules/(?P<server>.*):(?P<port>[0-9]+)$', 'views.rules'),
    url(r'^rules/(?P<server>.*)$', 'views.rules', kwargs={'port':25565})
)
