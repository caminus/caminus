from django.db.models.signals import post_save
from minecraft.models import PlayerSession, Server
from django.core.cache import cache
import badges.api
import events

def cachePlayerList():
    serverInfo = {}
    for s in Server.objects.all():
        playerList = []
        for p in s.online_players():
            playerList.append(p.mc_username)
        serverInfo[s.hostname] = {'players':playerList}
    cache.set('caminus-server-info', serverInfo, 30)

def update_player_lists(sender, instance, created, **kwargs):
    cachePlayerList()

post_save.connect(update_player_lists, sender=PlayerSession)

def notify_badge(sender, award, *args, **kwargs):
    player = award.user.minecraftprofile.mc_username
    events.server_broadcast("%s was awarded the %s badge!"%(player, award.badge.name))

badges.api.badge_awarded.connect(notify_badge)
