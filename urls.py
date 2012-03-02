from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'news.views.index', name='home'),
    url(r'^petitions/', include('petition.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^forums/', include('forums.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^i/(?P<code>.+)', 'profiles.views.claimInvite')
)

urlpatterns += staticfiles_urlpatterns()
