from django.db import models
from minecraft.models import MinecraftProfile

class VaultSlot(models.Model):
    player = models.ForeignKey(MinecraftProfile, related_name='vault_slots')
    item = models.IntegerField()
    quantity = models.IntegerField()
    damage = models.IntegerField()
    data = models.IntegerField()
