from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
import django.contrib.auth
from django.contrib.auth import authenticate, login
import forms

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
