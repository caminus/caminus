from __future__ import absolute_import

from django.db import models
from django.contrib.auth.models import User
import badges.api
from api.events import user_message
from notification import models as notification
from django.core.urlresolvers import reverse

from django.dispatch import dispatcher

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

class Badge(models.Model):
    name = models.TextField()
    description = models.TextField()
    slug = models.SlugField(blank=True)
    users = models.ManyToManyField(User, related_name='badges', through='Award', blank=True)
    secret = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        unique_slug(self, slug_source='name', slug_field='slug')
        super(Badge, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Award(models.Model):
    badge = models.ForeignKey(Badge)
    user = models.ForeignKey(User, related_name='awards')
    reason = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Award, self).save(*args, **kwargs)
        badges.api.badge_awarded.send_robust(sender=intern(str(self.badge.slug)), award=self)
        notification.send([self.user], "badge_awarded", {"award": self, 'notice_description': self.badge, 'notice_url': reverse('user_profile')})
        user_message(self.user, "You have been awarded the '%s' badge."%self.badge)

    def __unicode__(self):
        return "%s for %s"%(self.badge.__unicode__(), self.user.__unicode__())
