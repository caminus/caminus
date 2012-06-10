import badges.api
from PIL import Image
import os
from django.core.cache import cache
from urllib2 import urlopen
from httplib import HTTPException
from cStringIO import StringIO

def update_badges(user):
    playtime = user.minecraftprofile.totalPlaytime();
    if playtime.days >= 1:
        badges.api.award(user, "24h_playtime")
    if playtime.days >= 7:
        badges.api.award(user, "7d_playtime")
    if playtime.days >= 30:
        badges.api.award(user, "30d_playtime")

def download_avatar(username, size):
    avatar = cache.get('minecraft-avatar-%s-%s'%(username, size))
    size = int(size)
    if avatar is None:
        try:
            skinStream = urlopen("http://minecraft.net/skin/%s.png"%(username.replace(" ", "_")))
        except (IOError, HTTPException), e:
            skinStream = open(os.path.dirname(__file__)+"/static/skin.png")
        imgStream = StringIO(skinStream.read())
        img = Image.open(imgStream)
        face = img.crop((8, 8, 16,16))
        face.load()
        overlay = img.crop((40, 8, 48, 16))
        overlay.load()
        try:
            img = Image.composite(overlay, face, overlay)
        except ValueError, e:
            img = face
        img = img.resize((size, size), Image.NEAREST)
        buf = StringIO()
        img.save(buf, "PNG")
        avatar = buf.getvalue()
    cache.set('minecraft-avatar-%s-%s'%(username, size), avatar, 86400)
    return avatar
