from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import shortuuid

class Invite(models.Model):
    code = models.CharField(max_length=30)
    creator = models.ForeignKey(User, related_name='invites')
    claimer = models.OneToOneField(User, related_name='claimed_invite', blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = shortuuid.uuid()[:6].upper()
        super(Invite, self).save(*args, **kwargs)

    class Meta:
        ordering = ['deleted']

    @models.permalink
    def get_absolute_url(self):
        return ('profiles.views.claimInvite', [], {'code': self.code})
