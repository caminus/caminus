from django.conf.urls import patterns, url, include

urlpatterns = patterns('vault',
    url(r'^$', 'views.index'),
)
