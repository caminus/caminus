from django.db import models
from django.contrib.auth.models import User

class MinecraftProfile(models.Model):
    user = models.OneToOneField(User)
    mc_username = models.CharField(max_length=30)

    def __unicode__(self):
        return self.mc_username

class Quote(models.Model):
    text = models.CharField(max_length=50)

    def __unicode__(self):
        return self.text
