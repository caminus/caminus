from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView


urlpatterns = patterns('local',
    url(r'^me$', 'views.profile', name='user_profile'),
    url(r'^me/notifications/mark_read$', 'views.mark_notifications_read'),
    url(r'^user/(?P<username>.+)$', 'views.profile'),
    url(r'^player/(?P<mc_username>.+)$', 'views.profile'),
    url(r'^list$', 'views.list'),
    url(r'^welcome', TemplateView.as_view(template_name="welcome")),# direct_to_template, {'template': 'local/welcome.html'}, name='welcome'),
    url(r'^register', 'views.register'),
    url(r'^invites/claim$', 'views.claimInvite'),
    url(r'^invites/claim/(?P<code>.+)$', 'views.claimInvite'),
    url(r'^invites/delete/(?P<code>.+)$', 'views.deleteInvite'),
    url(r'^invites/new$', 'views.createInvite'),
    url(r'^invites$', 'views.invites'),
    url(r'^edit$', 'views.edit'),
    url(r'^disabled$', TemplateView.as_view(template_name="disabled_account")),#direct_to_template, {'template': 'local/disabled.html'}, name='disabled_account')
)
