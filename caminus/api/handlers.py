from piston.handler import AnonymousBaseHandler, BaseHandler
import time
from django.core.cache import cache
from django.conf import settings
from django.core.cache import cache
import appversion
from minecraft.models import MinecraftProfile
from local.models import Quote
from minecraft.models import MOTD, Server, PlayerSession
from django.db.models import F
from django.http import HttpResponse
from urllib2 import urlopen
import json
from datetime import datetime
from models import cachePlayerList
from events import server_queue, web_queue, chat, server_broadcast, send_web_event, QuitEvent, JoinEvent, PlayerDeathEvent
from bounty.models import Bounty
from vault.models import VaultSlot

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
            send_web_event(JoinEvent(playername))
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
            send_web_event(QuitEvent(playername))
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
        return {'identity': request.server, 'api-version': 2, 'server-version': appversion.version()}

class ServerEventHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT')

    def read(self, request):
        queue = server_queue(request.server)
        queue.watch('caminus-broadcast-%s'%request.server.id)
        events = []
        job = queue.reserve(timeout=30)
        while job:
          job.bury()
          events.append({'id': job.jid, 'event': json.loads(job.body)})
          job = queue.reserve(timeout=0)
        return {'events': events}

    def create(self, request):
        queue = server_queue(request.server)
        try:
            queue.delete(int(request.POST['job']))
        except Exception, e:
            pass
        return {'result': 'success'}

    def update(self, request):
        events = json.loads(request.POST['events'])['events']
        for evt in events:
            print repr(evt)
            if evt['type'] == 'chat':
                chat(evt['payload']['sender'], evt['payload']['message'])
            if evt['type'] == 'player-death':
              send_web_event(PlayerDeathEvent(evt['payload']['player'],
              evt['payload']['message']))
            if evt['type'] == 'player-murder':
              bounties = Bounty.objects.filter(target__mc_username=evt['payload']['player'])
              killer = MinecraftProfile.objects.get(mc_username=evt['payload']['killer'])
              for bounty in bounties:
                bounty.close(killer)
              if len(bounties) > 0:
                server_broadcast("The bounty on %s has been collected."%(evt['payload']['player']))
        return {'result': 'success'}

class ChatHandler(BaseHandler):
    allowed_methods = ('POST',)

    def create(self, request):
      chat(request.user.minecraftprofile.mc_username, request.POST['message'])
      server_broadcast("<%s> %s"%(request.user.minecraftprofile.mc_username,
        request.POST['message']))

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
        pollData['events'] = []
        pollData['poll-id'] = timestamp
        if timestamp == "0" and settings.CAMINUS_USE_BEANSTALKD:
          pollData['poll-id'] = time.time()
          latestEvents = cache.get('minecraft-web-events')
          if not latestEvents:
            latestEvents = []
          for e in latestEvents:
            pollData['events'].append(json.loads(e))
        else:
          eventQueue = web_queue(timestamp)
          event = eventQueue.reserve(timeout=30)
          if event:
            eventData = json.loads(event.body)
            pollData['events'].append(eventData['event'])
            event.delete()
        return pollData

class VaultHandler(BaseHandler):
    allowed_methods = ('PUT','GET')

    def read(self, request, playername):
        player = MinecraftProfile.objects.get(mc_username__exact=playername)
        items = []
        for slot in player.vault_slots.all():
            items.append({'item': slot.item, 'quantity':
              slot.quantity, 'damage': slot.damage, 'data': slot.data,
              'position': slot.position})
        return {'items': items}

    def update(self, request, playername):
        player = MinecraftProfile.objects.get(mc_username__exact=playername)
        vaultContents = json.loads(request.POST['contents'])['items']
        stacks = player.vault_slots.all()
        for stack in vaultContents:
          updated = False
          slot,created = VaultSlot.objects.get_or_create(player=player,
            position=stack['position'])
          if slot.item != stack['item']:
              slot.item = stack['item']
              updated = True
          if slot.quantity != stack['quantity']:
              slot.quantity = stack['quantity']
              updated = True
          if slot.damage != stack['damage']:
              slot.damage = stack['damage']
              updated = True
          if slot.data != stack['data']:
              slot.data = stack['data']
              updated = True
          if updated:
              print "Saving slot %s(%s): %s"%(slot.position, slot.id, slot.item)
              slot.save()
        return {'success': True}
