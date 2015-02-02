from django.conf.urls import patterns, url, include

urlpatterns = patterns('bounty',
    url(r'^$', 'views.index'),
    url(r'^create$', 'views.create'),
)

