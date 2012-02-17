from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('minecraft',
    url(r'^profile$', 'views.profile', name='user_profile'),
)
