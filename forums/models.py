from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

def unique_slug(item,slug_source,slug_field):
  """Ensures a unique slug field by appending an integer counter to duplicate slugs.
  
  The item's slug field is first prepopulated by slugify-ing the source field. If that value already exists, a counter is appended to the slug, and the counter incremented upward until the value is unique.
  
  For instance, if you save an object titled Daily Roundup, and the slug daily-roundup is already taken, this function will try daily-roundup-2, daily-roundup-3, daily-roundup-4, etc, until a unique value is found.
  
  Call from within a model's custom save() method like so:
  unique_slug(item, slug_source='field1', slug_field='field2')
  where the value of field slug_source will be used to prepopulate the value of slug_field.
  """
  if not getattr(item, slug_field): # if it's already got a slug, do nothing.
      from django.template.defaultfilters import slugify
      slug = slugify(getattr(item,slug_source))
      itemModel = item.__class__
      # the following gets all existing slug values
      allSlugs = [sl.values()[0] for sl in itemModel.objects.values(slug_field)]
      if slug in allSlugs:
          import re
          counterFinder = re.compile(r'-\d+$')
          counter = 2
          slug = "%s-%i" % (slug, counter)
          while slug in allSlugs:
              slug = re.sub(counterFinder,"-%i" % counter, slug)
              counter += 1
      setattr(item,slug_field,slug)

class Forum(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    name = models.CharField(max_length=30)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        unique_slug(self, slug_source='name', slug_field='slug')
        super(Forum, self).save(*args, **kwargs)

    def topicCount(self):
        return self.topic_set.count()

    def latestTopic(self):
        try:
            return self.topic_set.extra(order_by = ['created'])[0]
        except IndexError, e:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ('forums.views.forum', [self.slug])

    def __unicode__(self):
        return self.name

class Topic(models.Model):
    forum = models.ForeignKey(Forum)
    title = models.CharField(max_length=100)
    rootPost = models.OneToOneField('Post', related_name='parentTopic')
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)
    slug = models.SlugField(editable=False, blank=True)
    sticky = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sticky', '-updated']

    def save(self, *args, **kwargs):
        unique_slug(self, slug_source='title', slug_field='slug')
        super(Topic, self).save(*args, **kwargs)

    def lastPost(self):
        try:
            return self.rootPost.get_descendants(True).extra(order_by = ['updated'])[0]
        except IndexError, e:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ('forums.views.topic', [], {"forumSlug":self.forum.slug, "topicSlug":self.slug, "topicID":self.id})

    def __unicode__(self):
        return self.title

class Post(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    user = models.ForeignKey(User)
    body = models.TextField()
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)

    def topic(self):
        return self.get_root().parentTopic

    @models.permalink
    def get_absolute_url(self):
        return ('forums.views.post', [self.id])

    def __unicode__(self):
        return self.body
