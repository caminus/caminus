from PIL import Image
from django.http import HttpResponse
from urllib2 import urlopen
from cStringIO import StringIO
from django.core.cache import cache
from django.views.decorators.cache import cache_control

def avatar(request, username):
    avatar = cache.get('minecraft-avatar-%s'%(username))
    if avatar is None:
        imgStream = StringIO(urlopen("http://minecraft.net/skin/%s.png"%(username)).read())
        img = Image.open(imgStream)
        img = img.crop((8, 8, 16,16))
        img = img.resize((64, 64), Image.NEAREST)
        buf = StringIO()
        img.save(buf, "PNG")
        avatar = buf.getvalue()
    cache.set('minecraft-avatar-%s', avatar, 86400)
    return HttpResponse(avatar, content_type="image/png")
