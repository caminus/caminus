from django.db import models
import pyspy
from django.core.cache import cache
import socket

class Server(models.Model):
    hostname = models.CharField(max_length=100)
    port = models.IntegerField(default=25565)
    query_port = models.IntegerField(default=25565)

    class Meta:
        permissions = (
            ('login_all', 'Can login to all minecraft servers'),
        )

    def online_playaers(self):
        players = cache.get('minecraftPlayerList-%s:%s'%(self.hostname, self.query_port))
        if players is None:
            players = []
            try:
                client = pyspy.GamespyClient(server.hostname, server.query_port)
                client.update()
                pList = client.players()
                for p in pList:
                    try:
                        player = Player.objects.get(username__exact = p)
                    except ObjectDoesNotExist, e:
                        player = Player()
                        player.username = p
                cache.set('minecraftPlayerList-%s:%s'%(self.hostname, self.query_port), players, 120)
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
