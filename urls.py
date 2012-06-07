from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'local.views.index', name='home'),
    url(r'^petitions/', include('petition.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^minecraft/', include('minecraft.urls')),
    url(r'^mail/', include('messages.urls')),
    url(r'^profiles/', include('local.urls')),
    url(r'^users/(?P<username>.+)/', 'local.views.profile'),
    url(r'^players/(?P<mc_username>.+)$', 'local.views.profile'),
    url(r'^accounts/logout', 'django.contrib.auth.views.logout', kwargs={'next_page':'/'}),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^forums/', include('forums.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^notification/', include('notification.urls')),
    url(r'^i/(?P<code>.+)', 'local.views.claimInvite'),
    url(r'^donate/', include('donate.urls')),
    url(r'^f/(?P<id>.*)', 'forums.views.post'),
    url(r'^badges/', include('badges.urls')),
)

urlpatterns += staticfiles_urlpatterns()
