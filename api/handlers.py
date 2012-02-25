from piston.handler import AnonymousBaseHandler
from profiles.models import MinecraftProfile
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
