from piston.handler import AnonymousBaseHandler, BaseHandler
from profiles.models import MinecraftProfile, Quote
from minecraft.models import MOTD, Server
from django.http import HttpResponse
from urllib2 import urlopen
import json

class WhitelistHandler(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, username=None):
        if username:
            try:
                profile = MinecraftProfile.objects.all().filter(mc_username__iexact=username)[0]
            except IndexError, e:
                return HttpResponse(status=403)
            if profile.user.is_active:
                return HttpResponse(status=204)
        return HttpResponse(status=404)

class MOTDHandler(AnonymousBaseHandler):
    allowed_methods = ('GET',)
    
    def read(self, request, username):
        motd = "No MOTD configured!"
        motdList = MOTD.objects.all()
        if len(motdList) > 0:
            motd = motdList[0].text
        quote = Quote.objects.order_by('?')
        if len(quote) > 0:
            motd += "\n"+'"'+quote[0].text+'"'
        return {"motd":motd.split('\n')}

class BalanceHandler(BaseHandler):
    def read(self, request):
        user = request.user
        return {"balance":user.get_profile().currencyaccount.balance}

class ServerHandler(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, hostname):
        s = Server.objects.get(hostname__exact=hostname)
        try:
            dynMapJS = json.load(urlopen("http://%s/map/up/world/world/0"%(hostname)))
            serverTime = dynMapJS["servertime"]
        except Exception, e:
            serverTime = -1
        return {"hostname":hostname, "port":s.port, "players": map(lambda x:x.mc_username, s.online_players()), "time":serverTime}
