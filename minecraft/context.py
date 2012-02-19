import pyspy
from django.conf import settings

def server_info(request):
    client = pyspy.GamespyClient(settings.MINECRAFT_SERVER, settings.MINECRAFT_SERVER_PORT)
    client.update()
    return {'onlinePlayers':client.players(), 'minecraftHost': settings.MINECRAFT_SERVER, 'minecraftPort': settings.MINECRAFT_SERVER_PORT}
