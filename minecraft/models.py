from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
import pyspy
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
import socket

class MinecraftProfile(models.Model):
    user = models.OneToOneField(User)
    mc_username = models.CharField(max_length=30, verbose_name="Minecraft.net Username", unique=True)

    def serverPermissions(self):
        perms = []
        if self.user.is_staff:
            perms.append('bukkit.command.op.give')
        for group in self.user.groups.all():
            for perm in group.minecraftgroup.permissionList.split("\n"):
                perms.append(perm.strip())
        return perms

    def __unicode__(self):
        return self.mc_username

class Server(models.Model):
    hostname = models.CharField(max_length=100)
    port = models.IntegerField(default=25565)
    query_port = models.IntegerField(default=25565)
    ruleset = models.TextField(default='')
    secret = models.CharField(max_length=100)

    class Meta:
        permissions = (
            ('login_all', 'Can login to all minecraft servers'),
        )

    def online_players(self):
        players = cache.get('minecraftPlayerList-%s:%s'%(self.hostname, self.query_port))
        if players is None:
            players = []
            try:
                client = pyspy.GamespyClient(self.hostname, self.query_port)
                # FIXME: pyspy sometimes hangs here
                #client.update()
                pList = client.players()
                for p in pList:
                    try:
                        player = MinecraftProfile.objects.get(mc_username__exact = p)
                    except ObjectDoesNotExist, e:
                        player = MinecraftProfile()
                        player.mc_username = p
                cache.set('minecraftPlayerList-%s:%s'%(self.hostname, self.query_port), players, 10)
            except socket.error:
                pass
        return players

    def __unicode__(self):
        return "%s:%d"%(self.hostname, self.port)

class MOTD(models.Model):
    server = models.ForeignKey(Server)
    text = models.TextField()

    def __unicode__(self):
        return self.text

class PlayerSession(models.Model):
    server = models.ForeignKey(Server)
    player = models.ForeignKey(MinecraftProfile)
    ip = models.IPAddressField()
    start = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    end = models.DateTimeField(blank=True, null=True)

def create_profile(sender, instance, created, **kwargs):
    if created:
        MinecraftProfile.objects.create(user=instance, mc_username=instance.username)

post_save.connect(create_profile, sender=User)

class MinecraftGroup(models.Model):
    authGroup = models.OneToOneField(Group)
    permissionList = models.TextField(blank=True)

    def __unicode__(self):
        return self.authGroup.__unicode__()

def create_group(sender, instance, created, **kwargs):
    if created:
        MinecraftGroup.objects.create(authGroup = instance)

post_save.connect(create_group, sender=Group)
