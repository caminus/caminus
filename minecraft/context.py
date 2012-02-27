import pyspy
from django.conf import settings
from django.core.cache import cache

def server_info(request):
    players = cache.get('minecraftPlayerList')
    if players is None:
        try:
            client = pyspy.GamespyClient(settings.MINECRAFT_SERVER, settings.MINECRAFT_SERVER_PORT)
            client.update()
            players = client.players()
            cache.set('minecraftPlayerList', players, 120)
        except socket.error:
            pass
    return {'onlinePlayers':players, 'minecraftHost': settings.MINECRAFT_SERVER, 'minecraftPort': settings.MINECRAFT_SERVER_PORT}
