from django.http import HttpResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_control
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import select_template
from minecraft import download_avatar
import models

@cache_control(public=True, private=False, no_cache=False, no_transform=False, must_revalidate=False, proxy_revalidate=False, max_age=86400)
def avatar(request, username, size=64):
    avatar = download_avatar(username, size)
    return HttpResponse(avatar, content_type="image/png")

def rules(request, server, port):
    s = models.Server.objects.get(hostname__exact=server, port__exact=port)
    return render_to_response('minecraft/rules.html', {'server': s}, context_instance = RequestContext(request))
