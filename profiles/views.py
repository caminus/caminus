from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import django.contrib.auth
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
import forms
import models
import shortuuid
from minecraft.forms import ProfileForm

@login_required
def profile(request):
    return render_to_response('profiles/profile.html', context_instance = RequestContext(request))

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
        return HttpResponseRedirect(reverse('profiles.views.profile'))
    return render_to_response('profiles/edit.html', {"form":form}, context_instance = RequestContext(request))

@login_required
def invites(request):
    invites = request.user.invites.all()
    return render_to_response('profiles/invites.html', {'invites': invites}, context_instance = RequestContext(request))

@login_required
def createInvite(request):
    invite = models.Invite()
    invite.creator = request.user
    invite.code = shortuuid.uuid()[:6].upper()
    invite.save()
    return HttpResponseRedirect(reverse('profiles.views.invites'))

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
            user = django.contrib.auth.authenticate(userForm.cleaned_data['username'], userForm.cleaned_data['password'])
            django.contrib.auth.login(request, user)
            del request.session['profile-invite']
            return HttpResponseRedirect("/")
    return render_to_response('profiles/register.html', {'userForm': userForm, 'profileForm': profileForm, 'invite':invite}, context_instance = RequestContext(request))

@login_required
def deleteInvite(request, code=None):
    invite = models.Invite.objects.get(code__exact=code)
    if invite.claimer:
        return HttpResponseRedirect(reverse('profiles.views.invites'))
    if request.method == 'POST':
        invite.deleted = True
        invite.save()
        return HttpResponseRedirect(reverse('profiles.views.invites'))
    return render_to_response('profiles/delete_invite.html', {'invite':invite}, context_instance = RequestContext(request))

def claimInvite(request, code=None):
    if request.user.is_authenticated():
        invite = models.Invite.objects.get(code__exact=code)
        siteURL = Site.objects.get_current().domain
        return render_to_response('profiles/show_invite.html', {'invite':invite, 'site_url': siteURL}, context_instance = RequestContext(request))
    if request.method == 'POST':
        form = forms.InviteClaimForm(request.POST)
    else:
        form = forms.InviteClaimForm()
    if form.is_valid():
        code = form.cleaned_data['code']
    if code:
        invite = models.Invite.objects.get(code__exact=code)
        request.session['profile-invite'] = invite
        return HttpResponseRedirect(reverse('profiles.views.register'))
    return render_to_response('profiles/claim_invite.html', {'form': form}, context_instance = RequestContext(request))

def list(request):
    profiles = User.objects.all()
    return render_to_response('profiles/list.html', {'profiles': profiles}, context_instance = RequestContext(request))
