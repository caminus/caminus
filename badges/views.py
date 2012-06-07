import models
from django.shortcuts import render_to_response

def index(request):
    badges = models.Badge.objects.filter(secret=False)
    return render_to_response('badges/index.html', {'badges': badges})
