from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class MinecraftProfile(models.Model):
    user = models.OneToOneField(User)
    mc_username = models.CharField(max_length=30)

    def __unicode__(self):
        return self.mc_username

class Quote(models.Model):
    text = models.CharField(max_length=50)

    def __unicode__(self):
        return self.text

def create_profile(sender, instance, created, **kwargs):
    if created:
        MinecraftProfile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)
