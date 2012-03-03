from django.db import models
from profiles.models import MinecraftProfile
from django.db.models.signals import post_save

class CurrencyAccount(models.Model):
    profile = models.ForeignKey(MinecraftProfile, to_field='mc_username', db_column='username')
    balance = models.FloatField(default=3000)
    status = models.IntegerField()

    class Meta:
        db_table = 'iConomy'

    def __unicode__(self):
        return self.profile.__unicode__()

def create_account(sender, instance, created, **kwargs):
    if created:
        CurrencyAccount.objects.create(profile=sender)

post_save.connect(create_account, sender=MinecraftProfile)
