from django.conf.urls.defaults import patterns, include, url
urlpatterns = patterns('vault',
    url(r'^$', 'views.index'),
)
