import models
import forums.models
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from donate.models import Donation
from datetime import datetime
from django.conf import settings

def random_quote(request):
    quote = models.Quote.objects.order_by('?')
    if len(quote) > 0:
        return {'quote': quote[0]}
    return {}

def forum_activity(request):
    latestPosts = forums.models.Post.objects.all().order_by('-updated')[0:5]
    return {'latestForumPosts': latestPosts}

def login_form(request):
    return {'login_form': AuthenticationForm()}

def donation_info(request):
    now = datetime.now()
    monthStart = datetime(now.year, now.month, 1)
    donations = Donation.objects.filter(created__gt=monthStart).aggregate(Sum('quantity'))['quantity__sum']
    goal = getattr(settings, 'CAMINUS_DONATION_GOAL', 0)
    if donations > goal:
        progress = 100
    else:
        progress = donations/goal*100
    return {'donation_month_total': donations, 'donation_month_goal': goal, 'donation_goal_progress': progress}
