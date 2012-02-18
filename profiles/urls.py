from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('profiles',
    url(r'^me$', 'views.profile', name='user_profile'),
)
