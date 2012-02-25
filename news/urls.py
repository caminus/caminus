from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('news',
    url('^$', 'views.index'),
    url('^(?P<page>[0-9]+)$', 'views.index'),
    url('^(?P<slug>.*)$', 'views.view')
)
