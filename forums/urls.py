from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('forums',
    url(r'^$', 'views.index'),
    url(r'^forum/(?P<forum>.*)/$', 'views.forum'),
    url(r'^forum/(?P<forumID>.*)/new$', 'views.newTopic'),
    url(r'^forum/(?P<forumSlug>.*)/(?P<topicID>.*)/(?P<topicSlug>.*)$', 'views.topic'),
    url(r'^topic/(?P<topicID>.*)$', 'views.topic'),
    url(r'^reply/(?P<topicID>.*)', 'views.reply'),
    url(r'^reply$', 'views.reply'),
    url(r'^post/(?P<id>.*)$', 'views.post'),
)
