from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from notification import models as notification
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
import django.contrib.auth
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
import forms
import models
from forums.models import Forum
from minecraft.forms import ProfileForm
from minecraft.models import MinecraftProfile
from django.conf import settings

def profile(request, username=None, mc_username=None):
    if username is None and mc_username is None:
        user = request.user
    elif mc_username is None:
        user = User.objects.get(username=username)
    else:
        user = MinecraftProfile.objects.get(mc_username=mc_username).user
    return render_to_response('local/profile.html', {'profile': user}, context_instance = RequestContext(request))

@login_required
def edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.minecraftprofile)
    else:
        form = ProfileForm(instance=request.user.minecraftprofile)
    if form.is_valid():
        profile = request.user.minecraftprofile
        profile.mc_username = form.cleaned_data['mc_username']
        profile.save()
        return HttpResponseRedirect(reverse('local.views.profile'))
    return render_to_response('local/edit.html', {"form":form}, context_instance = RequestContext(request))

@login_required
def invites(request):
    invites = request.user.invites.all()
    return render_to_response('local/invites.html', {'invites': invites}, context_instance = RequestContext(request))

@login_required
def createInvite(request):
    activeCount = request.user.invites.exclude(deleted=True).filter(claimer=None)
    if len(activeCount) < settings.CAMINUS_MAX_INVITES:
        invite = models.Invite()
        invite.creator = request.user
        invite.save()
    else:
        messages.error(request, "You already have your maximum number of active invites.")
    return HttpResponseRedirect(reverse('local.views.invites'))

def register(request):
    invite = request.session['profile-invite']
    if request.method == 'POST':
        userForm = forms.UserForm(request.POST, prefix='user')
        profileForm = ProfileForm(request.POST, prefix='profile')
    else:
        userForm = forms.UserForm(prefix='user')
        profileForm = ProfileForm(prefix='profile')
    if userForm.is_valid() and profileForm.is_valid():
        oldUser = None
        try:
            oldUser = User.objects.get(username__exact=userForm.cleaned_data['username'])
        except ObjectDoesNotExist, e:
            pass
        if not oldUser:
            user = User.objects.create_user(userForm.cleaned_data['username'], userForm.cleaned_data['email'], userForm.cleaned_data['password'])
            user.save()
            invite.claimer = user
            invite.save()
            profile = user.minecraftprofile
            profile.mc_username = profileForm.cleaned_data['mc_username']
            profile.save()
            user = authenticate(username=userForm.cleaned_data['username'], password=userForm.cleaned_data['password'])
            notification.send_now([invite.creator], "invite_accepted", {"new_user": user})
            login(request, user)
            del request.session['profile-invite']
            return HttpResponseRedirect(reverse('welcome'))
    return render_to_response('local/register.html', {'userForm': userForm, 'member_count': len(User.objects.all()), 'profileForm': profileForm, 'invite':invite}, context_instance = RequestContext(request))

@login_required
def deleteInvite(request, code=None):
    invite = models.Invite.objects.get(code__exact=code)
    if invite.claimer:
        messages.error(request, "That invite is already claimed.")
        return HttpResponseRedirect(reverse('local.views.invites'))
    if request.method == 'POST':
        invite.deleted = True
        invite.save()
        messages.info(request, "Invite deleted.")
        return HttpResponseRedirect(reverse('local.views.invites'))
    return render_to_response('local/delete_invite.html', {'invite':invite}, context_instance = RequestContext(request))

def claimInvite(request, code=None):
    if request.user.is_authenticated():
        invite = models.Invite.objects.get(code__exact=code)
        siteURL = Site.objects.get_current().domain
        return render_to_response('local/show_invite.html', {'invite':invite, 'site_url': siteURL}, context_instance = RequestContext(request))
    if request.method == 'POST':
        form = forms.InviteClaimForm(request.POST)
    else:
        form = forms.InviteClaimForm()
    if form.is_valid():
        code = form.cleaned_data['code']
    if code:
        try:
            invite = models.Invite.objects.get(code__exact=code, claimer__exact=None, deleted__exact=False)
        except models.Invite.DoesNotExist:
            raise Http404
        request.session['profile-invite'] = invite
        return HttpResponseRedirect(reverse('local.views.register'))
    return render_to_response('local/claim_invite.html', {'form': form}, context_instance = RequestContext(request))

def list(request):
    profiles = User.objects.all()
    groups = Group.objects.all()
    return render_to_response('local/list.html', {'profiles': profiles, 'groups': groups}, context_instance = RequestContext(request))

def index(request):
    newsForum = Forum.objects.get(id=settings.CAMINUS_NEWS_FORUM_ID)
    try:
        latestNews = newsForum.topic_set.order_by('-created')[0]
    except IndexError, e:
        latestNews = None
    forums = Forum.objects.filter(parent=None)
    return render_to_response('local/index.html', {'news': latestNews, 'forums': forums}, context_instance = RequestContext(request))

@login_required
def mark_notifications_read(request):
    for notice in notification.Notice.objects.notices_for(request.user, unseen=True):
        notice.unseen = False
        notice.save()
    return HttpResponseRedirect(reverse('user_profile'))
