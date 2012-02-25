from piston.handler import AnonymousBaseHandler
from profiles.models import MinecraftProfile

class WhitelistHandler(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, username=None):
        if username:
            try:
                profile = MinecraftProfile.objects.get(mc_username__iexact=username)
            except Exception, e:
                return False
            return profile.user.is_active
        return False
