import models
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
  vault = models.VaultSlot.objects.filter(player=request.user.minecraftprofile)
  return render_to_response('vault/index.html', {'vault': vault},
      context_instance = RequestContext(request))
