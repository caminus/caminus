from piston.handler import AnonymousBaseHandler, BaseHandler
from django.core.cache import cache
from minecraft.models import MinecraftProfile
from local.models import Quote
from minecraft.models import MOTD, Server
from django.http import HttpResponse
from urllib2 import urlopen
import json

class WhitelistHandler(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, username):
        try:
            profile = MinecraftProfile.objects.all().filter(mc_username__iexact=username)[0]
        except IndexError, e:
            return {'valid': False, 'error': 'User not found'}
        if profile.user.is_active:
            return {'valid': True, 'error': ''}

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
        if user.is_anonymous():
            return HttpResponse(status=403)
        else:
            return {"balance":user.minecraftprofile.currencyaccount.balance}

class ServerHandler(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, hostname):
        s = Server.objects.get(hostname__exact=hostname)
        serverTime = cache.get('minecraftServerTime-%s:%s'%(s.hostname, s.port))
        playerList = []
        if serverTime is None:
            try:
                dynMapJS = json.load(urlopen("http://%s/map/up/world/world/0"%(hostname)))
                serverTime = dynMapJS["servertime"]
                playerList = dynMapJS["players"]
                cache.set('minecraftServerTime-%s:%s'%(s.hostname, s.port), serverTime, 120)
            except Exception, e:
                serverTime = -1
        return {"hostname":hostname, "port":s.port, "players": playerList, "time":serverTime, "rules": s.ruleset.split('\n')}
