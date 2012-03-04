from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('minecraft',
    url(r'^avatar/(?P<username>.*).png$', 'views.avatar'),
)
