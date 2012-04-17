import models
import forums.models
from django.contrib.auth.forms import AuthenticationForm

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
