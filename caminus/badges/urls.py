from django.conf.urls import patterns, url, include

urlpatterns = patterns('badges',
    url(r'^$', 'views.index'),
)
