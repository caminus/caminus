from PIL import Image
from django.http import HttpResponse
from urllib2 import urlopen
from cStringIO import StringIO
from django.core.cache import cache
from django.views.decorators.cache import cache_control
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import select_template
from httplib import HTTPException
import models
import os

def avatar(request, username, size=64):
    avatar = cache.get('minecraft-avatar-%s-%s'%(username, size))
    size = int(size)
    if avatar is None:
        try:
            skinStream = urlopen("http://minecraft.net/skin/%s.png"%(username.replace(" ", "_")))
        except (IOError, HTTPException), e:
            skinStream = open(os.path.dirname(__file__)+"/static/skin.png")
        imgStream = StringIO(skinStream.read())
        img = Image.open(imgStream)
        img = img.crop((8, 8, 16,16))
        img = img.resize((size, size), Image.NEAREST)
        buf = StringIO()
        img.save(buf, "PNG")
        avatar = buf.getvalue()
    cache.set('minecraft-avatar-%s-%s'%(username, size), avatar, 86400)
    return HttpResponse(avatar, content_type="image/png")

def rules(request, server, port):
    s = models.Server.objects.get(hostname__exact=server, port__exact=port)
    return render_to_response('minecraft/rules.html', {'server': s}, context_instance = RequestContext(request))
