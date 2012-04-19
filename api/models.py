from django.db.models.signals import post_save
from minecraft.models import PlayerSession, Server
from django.core.cache import cache

def cachePlayerList():
    serverInfo = {}
    for s in Server.objects.all():
        playerList = []
        for p in s.online_players():
            playerList.append(p.name)
        serverInfo[s.hostname] = {'players':playerList}
    cache.set('caminus-server-info', serverInfo, 30)

def update_player_lists(sender, instance, created, **kwargs):
    cachePlayerList()

post_save.connect(update_player_lists, sender=PlayerSession)
