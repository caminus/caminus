from django.conf.urls import patterns, url, include

urlpatterns = patterns('petition',
    url('^$', 'views.index'),
    url('^create$', 'views.create'),
    url('^(?P<id>[0-9]+)/close', 'views.close'),
    url('^(?P<id>[0-9]+)', 'views.view'),
    url('^comment/(?P<id>[0-9]+)', 'views.comment'),
)
