import models

def server_info(request):
    return {'minecraft_servers': models.Server.objects.all()}
