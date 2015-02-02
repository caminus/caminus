from django.conf.urls import patterns, url, include

urlpatterns = patterns('forums',
    url(r'^$', 'views.index'),
    url(r'^(?P<forum>.*)/$', 'views.forum'),
    url(r'^(?P<forumID>.*)/new$', 'views.newTopic'),
    url(r'^(?P<forumSlug>.*)/(?P<topicID>.*)/(?P<topicSlug>.*)$', 'views.topic'),
    url(r'^delete/(?P<topicID>.*)', 'views.deleteTopic'),
    url(r'^topic/(?P<topicID>.*)$', 'views.topic'),
    url(r'^sticky/(?P<topicID>.*)', 'views.stickyTopic'),
    url(r'^reply/(?P<topicID>.*)', 'views.reply'),
    url(r'^reply$', 'views.reply'),
    url(r'^edit/(?P<postID>.*)', 'views.editPost'),
    url(r'^edit$', 'views.editPost'),
    url(r'^post/(?P<id>.*)$', 'views.post'),
    url(r'^preview$', 'views.preview'),
)
