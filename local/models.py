from django.db import models
from minecraft.models import MinecraftProfile
from django.db.models.signals import post_save

class CurrencyAccount(models.Model):
    profile = models.OneToOneField(MinecraftProfile)
    username = models.CharField(max_length=255, unique=True, null=True)
    balance = models.FloatField(default=3000)
    status = models.IntegerField(default=0)

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.profile.mc_username
        super(CurrencyAccount, self).save(*args, **kwargs)

class Quote(models.Model):
    text = models.CharField(max_length=50)

    def __unicode__(self):
        return self.text

def create_account(sender, instance, created, **kwargs):
    if created:
        CurrencyAccount.objects.create(profile=instance)

post_save.connect(create_account, sender=MinecraftProfile)
