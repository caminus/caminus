from django.db import models
from minecraft.models import MinecraftProfile
from django.db.models.signals import post_save, post_delete
from api.events import VaultContentsEvent, broadcast_server_event
from minecraft.items import ITEMS

class VaultSlot(models.Model):
    player = models.ForeignKey(MinecraftProfile, related_name='vault_slots')
    item = models.IntegerField(default=0)
    quantity = models.IntegerField(default=-1)
    damage = models.IntegerField(default=0)
    data = models.IntegerField(default=0)
    position = models.IntegerField()

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return "%s.%s: %s %s"%(self.player, self.position, self.quantity, self.item)

    def name(self):
        name = self.metadata['name'].lower().split('_')
        return ' '.join(map(lambda x:x[0].upper()+x[1:], name))

    @property
    def metadata(self):
        for i in ITEMS:
          if i['id'] == self.item:
            return i;

    def damagePct(self):
      if self.metadata['durability'] == 0:
        return 100
      return round((float(self.damage)/float(self.metadata['durability']))*100)

def send_vault_delete(sender, instance, *args, **kwargs):
  slots = [
    {
      'item': None,
      'quantity': -1,
      'damage': None,
      'data': None,
      'position': instance.position
    }
  ]
  broadcast_server_event(VaultContentsEvent(instance.player.mc_username,
    slots))

def send_vault_update(sender, instance, created, *args, **kwargs):
  if created and instance.quantity == -1:
    return
  slots = [
    {
      'item': instance.item,
      'quantity': instance.quantity,
      'damage': instance.damage,
      'data': instance.data,
      'position': instance.position
    }
  ]
  broadcast_server_event(VaultContentsEvent(instance.player.mc_username, slots))

post_save.connect(send_vault_update, sender=VaultSlot, dispatch_uid='derp')
post_delete.connect(send_vault_delete, sender=VaultSlot, dispatch_uid='derp')
