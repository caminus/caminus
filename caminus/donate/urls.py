from django.conf.urls import patterns, url, include

urlpatterns = patterns('donate',
    url(r'^$', 'views.index'),
    url(r'^dwolla$', 'views.dwollaCallback'),
    url(r'^thanks/(?P<donation>.+)$', 'views.thanks'),
)
