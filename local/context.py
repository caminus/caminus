import models
import forums.models
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from donate.models import Donation
from datetime import datetime
from django.conf import settings
from notification.models import Notice
from django.core.urlresolvers import reverse

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
    donations = Donation.objects.filter(created__gt=monthStart).aggregate(Sum('quantity'))
    goal = getattr(settings, 'CAMINUS_DONATION_GOAL', 0)
    donationTotal = donations['quantity__sum']
    if donationTotal is None:
        progress = 0
        donationTotal = 0
    if donationTotal > goal or goal == 0:
        progress = 100
    else:
        progress = donationTotal/goal*100
    return {'donation_month_total': donationTotal, 'donation_month_goal': goal, 'donation_goal_progress': progress}

def notifications(request):
    if request.user.is_authenticated():
        return {'notices': Notice.objects.filter(unseen=True, user=request.user, on_site=True)}
    return {}

def javascript_uris(request):
    uris = (
      'local.views.mark_notifications_read',
    )
    ret = []
    for u in uris:
        ret.append({'name':u, 'uri':reverse(u)})
    return {'js_uris': ret}
