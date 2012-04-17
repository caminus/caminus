from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('local',
    url(r'^me$', 'views.profile', name='user_profile'),
    url(r'^list$', 'views.list'),
    url(r'^welcome', direct_to_template, {'template': 'local/welcome.html'}, name='welcome'),
    url(r'^register', 'views.register'),
    url(r'^invites/claim$', 'views.claimInvite'),
    url(r'^invites/claim/(?P<code>.+)$', 'views.claimInvite'),
    url(r'^invites/delete/(?P<code>.+)$', 'views.deleteInvite'),
    url(r'^invites/new$', 'views.createInvite'),
    url(r'^invites$', 'views.invites'),
    url(r'^edit$', 'views.edit'),
    url(r'^disabled$', direct_to_template, {'template': 'local/disabled.html'}, name='disabled_account')
)
