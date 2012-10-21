from django.conf.urls.defaults import patterns, include, url
from piston.resource import Resource
import handlers
from minecraft.models import Server
import hashlib
from django.http import HttpResponse

motdHandler = Resource(handlers.MOTDHandler)

class ServerAuther(object):
    def is_authenticated(self, request):
        authstring  = request.META.get("HTTP_AUTHORIZATION", None)
        if not authstring:
            return False
        authmeth, auth = authstring.split(' ', 1)
        if not authmeth.lower() == 'x-caminus':
            return False
        serverName,salt,token = auth.split('$', 2)
        try:
            server = Server.objects.get(hostname=serverName)
        except Server.DoesNotExist, e:
            return False
        tokenHash = hashlib.sha1()
        tokenHash.update("%s%s%s"%(serverName, salt, server.secret))
        if tokenHash.hexdigest() == token:
            request.server = server
            return True
        return False

    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp["WWW-Authenticate"] = 'X-Caminus realm=API'
        resp.status_code = 401
        return resp

class ServerResource(Resource):
    def __init__(self, handler):
        super(ServerResource, self).__init__(handler, ServerAuther())
        self.csrf_exempt  = getattr(self.handler, 'csrf_exempt', True)

urlpatterns = patterns('api',
    url(r'^motd/(?P<username>.*)$', motdHandler),
    url(r'^server/whoami$', ServerResource(handlers.ServerPingHandler)),
    url(r'^server/events$', ServerResource(handlers.ServerEventHandler)),
    url(r'^server/economy/(?P<playername>.*)$', ServerResource(handlers.EconomyHandler)),
    url(r'^server/session/(?P<playername>.*)/new$', ServerResource(handlers.NewPlayerSessionHandler)),
    url(r'^server/session/(?P<playername>.*)/close$', ServerResource(handlers.ClosePlayerSessionHandler)),
    url(r'^poll/(?P<timestamp>[0-9]+)$', Resource(handlers.PollHandler)),
)
