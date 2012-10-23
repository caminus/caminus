import models
from django.shortcuts import render_to_response

def index(request):
    bounties = models.Bounty.objects.filter(closed__isnull=True)
    return render_to_response('bounty/index.html', {'bounties': bounties})

def create(request):
    return render_to_response('bounty/create.html')
