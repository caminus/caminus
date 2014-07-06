from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('badges',
    url(r'^$', 'views.index'),
)
