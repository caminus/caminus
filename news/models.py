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

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(blank=True)
    author = models.ForeignKey(User, related_name='news_posts')
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('news.views.view', [], {'slug':self.slug})

    def save(self, *args, **kwargs):
        unique_slug(self, slug_source='title', slug_field='slug')
        super(Post, self).save(*args, **kwargs)

class Comment(MPTTModel):
    post = models.ForeignKey(Post, blank=True, null=True, related_name='comments')
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    author = models.ForeignKey(User)
    body = models.TextField()
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)

    def news_post(self):
        if self.parent is None:
            return self.post
        return self.get_root().post

    def __unicode__(self):
        return self.body
