from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('donate',
    url(r'^$', 'views.index'),
    url(r'^dwolla$', 'views.dwollaCallback'),
    url(r'^thanks/(?P<donation>.+)$', 'views.thanks'),
)
