from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import django.contrib.auth
from django.contrib.auth import authenticate, login
import forms
import models
import shortuuid

@login_required
def profile(request):
    return render_to_response('profiles/profile.html', context_instance = RequestContext(request))

@login_required
def edit(request):
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, instance=request.user.get_profile())
    else:
        form = forms.ProfileForm(instance=request.user.get_profile())
    if form.is_valid():
        profile = request.user.get_profile()
        profile.mc_username = form.cleaned_data['mc_username']
        profile.save()
        return HttpResponseRedirect(reverse('profiles.views.profile'))
    return render_to_response('profiles/edit.html', {"form":form}, context_instance = RequestContext(request))

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect("/")

def login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
    else:
        form = forms.LoginForm()
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django.contrib.auth.login(request, user)
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect(reverse('disabled_account'))
    return render_to_response('profiles/login.html', {"login_form":form}, context_instance = RequestContext(request))

@login_required
def invites(request):
    invites = request.user.invites.all()
    return render_to_response('profiles/invites.html', {'invites': invites}, context_instance = RequestContext(request))

@login_required
def createInvite(request):
    invite = models.Invite()
    invite.creator = request.user
    invite.code = shortuuid.uuid()[:6]
    invite.save()
    return HttpResponseRedirect(reverse('profiles.views.invites'))

def register(request):
    invite = request.session['profile-invite']
    if request.method == 'POST':
        userForm = forms.UserForm(request.POST, prefix='user')
        profileForm = forms.ProfileForm(request.POST, prefix='profile')
    else:
        userForm = forms.UserForm(prefix='user')
        profileForm = forms.ProfileForm(prefix='profile')
    if userForm.is_valid() and profileForm.is_valid():
        user = User()
        user.username = userForm.cleaned_data['username']
        user.email = userForm.cleaned_data['email']
        user.set_password(userForm.cleaned_data['password'])
        user.save()
        invite.claimer = user
        invite.save()
        profile = user.get_profile()
        profile.mc_username = profileForm.cleanedData['mc_username']
        profile.save()
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
