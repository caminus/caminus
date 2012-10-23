from django.db import models
from django.db.models import F
import datetime
from minecraft.models import MinecraftProfile
from api import events

class Bounty(models.Model):
  creator = models.ForeignKey(MinecraftProfile, related_name='created_bounties')
  killer = models.ForeignKey(MinecraftProfile, related_name='closed_bounties', null=True, blank=True)
  target = models.ForeignKey(MinecraftProfile, related_name='bounties')
  price = models.IntegerField()
  created = models.DateTimeField(auto_now_add=True)
  closed = models.DateTimeField(null=True, blank=True)

  def close(self, killer):
    self.closed = datetime.datetime.now()
    self.killer = killer
    self.save()
    killer.currencyaccount.balance = F('balance') + self.price
    killer.currencyaccount.save()
