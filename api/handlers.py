from piston.handler import AnonymousBaseHandler, BaseHandler
from django.core.cache import cache
from minecraft.models import MinecraftProfile
from local.models import Quote
from minecraft.models import MOTD, Server, PlayerSession
from django.db.models import F
from django.http import HttpResponse
from urllib2 import urlopen
import json
from datetime import datetime
from models import cachePlayerList
from events import server_queue

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

class NewPlayerSessionHandler(BaseHandler):
    allowed_methods = ('POST',)

    def create(self, request, playername):
        try:
            profile = MinecraftProfile.objects.all().filter(mc_username__iexact=playername)[0]
        except IndexError, e:
            return {'success': False, 'error': 'User not found', 'permissions': []}
        if profile.user.is_active:
            if profile.isBanned():
                return {'success': False, 'error': 'Your account is banned.', 'permissions': []}
            ip = request.POST['ip']
            server = request.server
            profile = MinecraftProfile.objects.get(mc_username__exact=playername)
            session = PlayerSession.objects.create(server=server, player=profile, ip=ip)
            return {'success': True, 'error': '', 'permissions': profile.serverPermissions(), 'sessionId': session.id}
        else:
            return {'success': False, 'error': 'Your account is inactive.', 'permissions': []}

class ClosePlayerSessionHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, playername):
        sessions = PlayerSession.objects.all().filter(player__mc_username__iexact=playername, end=None)
        for session in sessions:
            session.end = datetime.now()
            session.save()
        return {'valid': True}

class EconomyHandler(BaseHandler):
    allowed_methods = ('PUT','GET')

    def read(self, request, playername):
        player = MinecraftProfile.objects.get(mc_username__exact=playername)
        return {'balance': player.currencyaccount.balance}

    def update(self, request, playername):
        player = MinecraftProfile.objects.get(mc_username__exact=playername)
        delta = request.POST['delta']
        newBalance = player.currencyaccount.balance+float(delta)
        if newBalance >= 0:
            player.currencyaccount.balance = F('balance')+float(delta)
            player.currencyaccount.save()
            return {'success': True, 'balance': newBalance, 'message': ""}
        else:
            return {'success': False, 'balance': player.currencyaccount.balance, 'message': "Insufficient balance"}

class ServerPingHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        return {'identity': request.server}

class ServerEventHandler(BaseHandler):
    allowed_methods = ('GET', 'POST')

    def read(self, request):
        queue = server_queue(request.server)
        queue.watch('caminus-broadcast-%s'%request.server.id)
        events = []
        job = queue.reserve(timeout=30)
        if job:
          events.append({'id': job.jid, 'event': json.loads(job.body)})
        return {'events': events}

    def create(self, request):
        queue = server_queue(request.server)
        queue.delete(int(request.POST['job']))
        return {'result': 'success'}

class PollHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, timestamp):
        serverInfo = cache.get('caminus-server-info')
        if serverInfo == None:
            cachePlayerList()
        pollData = {'server-info': {}, 'user-info': {}}
        pollData['server-info'] = cache.get('caminus-server-info')
        if not request.user.is_anonymous():
            pollData['user-info']['balance'] = request.user.minecraftprofile.currencyaccount.balance
        return pollData
