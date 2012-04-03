from django.conf.urls.defaults import patterns, include, url
from django.contrib.syndication.views import Feed
import models

class NewsFeed(Feed):
    title = 'Caminus News'
    link = '/news/'
    description = 'News posts from Team Caminus'
    description_template = 'news/_feed_description.html'

    def items(self):
        return models.Post.objects.order_by('-created').filter(published=True)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_author_name(self, item):
        return item.author


urlpatterns = patterns('news',
    url('^$', 'views.index'),
    url('^comment/p/(?P<id>[0-9]+)$', 'views.comment'),
    url('^comment/c/(?P<parent>[0-9]+)$', 'views.comment'),
    url('^feed$', NewsFeed()),
    url('^(?P<page>[0-9]+)$', 'views.index'),
    url('^(?P<slug>.*)$', 'views.view')
)
