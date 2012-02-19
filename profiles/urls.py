from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('profiles',
    url(r'^me$', 'views.profile', name='user_profile'),
    url(r'^edit$', 'views.edit'),
    url(r'^login$', 'views.login'),
    url(r'^logout$', 'views.logout'),
    url(r'^disabled$', direct_to_template, {'template': 'profiles/disabled.html'}, name='disabled_account')
)
