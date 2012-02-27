from piston.handler import AnonymousBaseHandler
from profiles.models import MinecraftProfile, Quote
from minecraft.models import MOTD
from django.http import HttpResponse

class WhitelistHandler(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, username=None):
        if username:
            try:
                profile = MinecraftProfile.objects.get(mc_username__iexact=username)
            except Exception, e:
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
