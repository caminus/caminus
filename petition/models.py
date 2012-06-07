from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    author = models.ForeignKey(User, related_name='petitions')
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)
    body = models.TextField()
    closed = models.BooleanField(default=False)
    
    @models.permalink
    def get_absolute_url(self):
        return ('petition.views.view', [], {'id': self.id})

    def __unicode__(self):
        return self.body

class Comment(models.Model):
    author = models.ForeignKey(User, related_name='petition_comments')
    petition = models.ForeignKey(Petition)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)
    body = models.TextField()

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return self.body
