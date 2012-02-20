from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class MinecraftProfile(models.Model):
    user = models.OneToOneField(User)
    mc_username = models.CharField(max_length=30, verbose_name="Minecraft.net Username")

    def __unicode__(self):
        return self.mc_username


class Invite(models.Model):
    code = models.CharField(max_length=30)
    creator = models.ForeignKey(User, related_name='invites')
    claimer = models.OneToOneField(User, related_name='claimed_invite', blank=True, null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('profiles.views.claimInvite', [], {'code': self.code})

class Quote(models.Model):
    text = models.CharField(max_length=50)

    def __unicode__(self):
        return self.text

def create_profile(sender, instance, created, **kwargs):
    if created:
        MinecraftProfile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)
