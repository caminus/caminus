from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
import socket
import datetime

class MinecraftProfile(models.Model):
    user = models.OneToOneField(User)
    mc_username = models.CharField(max_length=30, verbose_name="Minecraft.net Username", unique=True)

    def isBanned(self):
        if self.bans.filter(expiration__gt=datetime.datetime.today()):
            return True
        if self.bans.filter(expiration__isnull=True):
            return True
        return False

    def serverPermissions(self):
        perms = []
        for group in self.user.groups.all():
            for perm in group.minecraftgroup.permissionList.split("\n"):
                perms.append(perm.strip())
        return perms

    def totalPlaytime(self):
        total = datetime.datetime.now()-datetime.datetime.now()
        for session in self.playersession_set.all():
            if not session.end:
                end = datetime.datetime.now()
            else:
                end = session.end
            total = total + end-session.start
        return total

    def averagePlaytime(self):
        if len(self.playersession_set.all()) == 0:
            return datetime.datetime.now()-datetime.datetime.now();
        return self.totalPlaytime()/len(self.playersession_set.all())

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
        activeSessions = PlayerSession.objects.all().filter(end=None)
        players = []
        for s in activeSessions:
            players.append(s.player)
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
        MinecraftProfile.objects.get_or_create(user=instance, mc_username=instance.username)

post_save.connect(create_profile, sender=User)

class MinecraftGroup(models.Model):
    authGroup = models.OneToOneField(Group)
    permissionList = models.TextField(blank=True)

    def __unicode__(self):
        return self.authGroup.__unicode__()

def create_group(sender, instance, created, **kwargs):
    if created:
        MinecraftGroup.objects.get_or_create(authGroup = instance)

post_save.connect(create_group, sender=Group)

class Ban(models.Model):
    player = models.ForeignKey(MinecraftProfile, related_name='bans')
    banner = models.ForeignKey(User)
    start = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(blank=True)
    reason = models.TextField()

    def __unicode__(self):
        return "%s: %s"%(self.player, self.reason)
