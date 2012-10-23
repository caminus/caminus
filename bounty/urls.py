from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('bounty',
    url(r'^$', 'views.index'),
    url(r'^create$', 'views.create'),
)

