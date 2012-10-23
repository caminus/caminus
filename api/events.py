from django.conf import settings
from django.core.cache import cache
from minecraft.models import Server
from json import dumps, JSONEncoder
import beanstalkc
from django.contrib.auth.models import User

class EventEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            return {'type': obj.type, 'payload': obj.data}
        return super(EventEncoder, self).default(obj)
            

class Event(object):
    def __init__(self, type, data):
        self.type = type
        self.data = data

class ChatEvent(Event):
    def __init__(self, sender, message):
      super(ChatEvent, self).__init__(type='chat', data={'sender': sender,
        'message': message})

class QuitEvent(Event):
  def __init__(self, player):
    super(QuitEvent, self).__init__(type='quit', data={'player': player})

class JoinEvent(Event):
  def __init__(self, player):
    super(JoinEvent, self).__init__(type='join', data={'player': player})

class BroadcastEvent(Event):
    def __init__(self, message):
        super(BroadcastEvent, self).__init__(type='broadcast', data={'message':
          message})

class PlayerMessageEvent(Event):
    def __init__(self, user, message):
        super(PlayerMessageEvent, self).__init__(type='player-message',
            data={'message': message, 'player': user})

def server_queue(server, users=[]):
    queueName = 'caminus-broadcast-%s'%server.id
    queue = beanstalkc.Connection(host=settings.CAMINUS_BEANSTALKD_HOST,
        port=settings.CAMINUS_BEANSTALKD_PORT)
    queue.use(queueName)
    queue.watch(queueName)
    if len(users) > 0:
        for user in users:
            queue.watch("caminus-user-%s"%user)
    return queue

def send_server_event(server, event):
    if settings.CAMINUS_USE_BEANSTALKD:
        queue = server_queue(server)
        json = dumps(event, cls=EventEncoder)
        queue.put(json)

def server_broadcast(message, *args):
    message = message%args
    for server in Server.objects.all():
      event = BroadcastEvent(message)
      send_server_event(server, event)

def user_message(user, message, *args):
    player = user.minecraftprofile.mc_username
    player_message(player, message, *args)

def player_message(playername, message, *args):
    message = message%args
    for server in Server.objects.all():
      event = PlayerMessageEvent(playername, message)
      send_server_event(server, event)

def web_queue(id):
    queueName = 'caminus-web-%s'%id
    queue = beanstalkc.Connection(host=settings.CAMINUS_BEANSTALKD_HOST,
        port = settings.CAMINUS_BEANSTALKD_PORT)
    queue.use(queueName)
    queue.watch(queueName)
    return queue

def send_web_event(event):
   latest = cache.get('minecraft-web-events')
   if latest is None:
     latest = []
   latest.append(dumps(event, cls=EventEncoder))
   while len(latest) > 10:
     latest.pop(0)
   cache.set('minecraft-web-events', latest, 86400);
   print 'cache:', latest
   if settings.CAMINUS_USE_BEANSTALKD:
     queue = beanstalkc.Connection(host=settings.CAMINUS_BEANSTALKD_HOST,
         port = settings.CAMINUS_BEANSTALKD_PORT)
     json = dumps(event, cls=EventEncoder)
     for tube in queue.tubes():
       if tube.startswith("caminus-web-"):
         queue.use(tube)
         queue.put(json)

def chat(playername, message):
  evt = ChatEvent(playername, message)
  send_web_event(evt)
