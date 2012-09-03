from django.conf import settings
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
