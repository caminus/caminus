import models
import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User 
from notification import models as notification
from django.contrib import messages
from api.events import user_message

@login_required
def create(request):
    if request.method == 'POST':
        form = forms.PetitionForm(request.POST)
    else:
        form = forms.PetitionForm()
    if form.is_valid():
        petition = models.Petition()
        petition.author = request.user
        petition.body = form.cleaned_data['body']
        petition.save()
        adminUsers = User.objects.filter(is_staff=True)
        notification.send(adminUsers, "petition_opened", {"petition": petition, 'notice_url': reverse('petition.views.view', kwargs={'id':petition.id}),'notice_description': petition.id})
        for user in adminUsers:
            user_message(user, "%s has opened a petition."%(request.user))
        messages.info(request, "Petition created.")
        return HttpResponseRedirect(reverse('petition.views.view', kwargs={"id":petition.id}))
    return render_to_response('petition/create.html', {'form':form}, context_instance = RequestContext(request))

@login_required
def index(request):
    if request.user.is_staff or request.user.is_superuser:
        openPetitions = models.Petition.objects.filter(closed=False)
        closedPetitions = models.Petition.objects.filter(closed=True)
    else:
        openPetitions = models.Petition.objects.filter(closed=False, author=request.user)
        closedPetitions = models.Petition.objects.filter(closed=True, author=request.user)
    return render_to_response('petition/index.html', {'openPetitions': openPetitions, 'closedPetitions': closedPetitions}, context_instance = RequestContext(request))

@login_required
def view(request, id):
    petition = models.Petition.objects.get(id__exact=id)
    commentForm = forms.CommentForm()
    return render_to_response('petition/view.html', {'petition':petition, 'form': commentForm}, context_instance = RequestContext(request))

def comment(request, id):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
    else:
        form = forms.CommentForm()
    if form.is_valid():
        petition = models.Petition.objects.get(id__exact=id)
        comment = models.Comment()
        comment.author = request.user
        comment.body = form.cleaned_data['body']
        comment.petition = petition
        comment.save()
        adminUsers = User.objects.filter(is_staff=True)
        for user in adminUsers:
            user_message(user, "%s has opened a petition."%(request.user))
        notification.send(adminUsers, "petition_commented", {"petition": petition, 'notice_url': reverse('petition.views.view', kwargs={'id':petition.id}),'notice_description': petition.id, 'comment': comment})
        if comment.author != petition.author:
            notification.send([petition.author], "petition_commented", {"petition": petition, 'notice_url': reverse('petition.views.view', kwargs={'id':petition.id}),'notice_description': petition.id, 'comment': comment})
        messages.info(request, "Comment added.")
        return HttpResponseRedirect(reverse('petition.views.view', kwargs={"id":petition.id})+"#c"+str(comment.id))

@login_required
def close(request, id):
    petition = models.Petition.objects.get(id__exact=id)
    petition.closed = True
    petition.save()
    if petition.author != request.user:
        user_notification(petition.author, "One of your petitions has been closed.")
        notification.send([petition.author], "petition_closed", {"petition": petition, 'notice_url': reverse('petition.views.view', kwargs={'id':petition.id}),'notice_description': petition.id})
    adminUsers = User.objects.filter(is_staff=True)
    notification.send([adminUsers], "petition_closed", {"petition": petition, 'notice_url': reverse('petition.views.view', kwargs={'id':petition.id}),'notice_description': petition.id})
    messages.info(request, "Petition closed.")
    return HttpResponseRedirect(reverse('petition.views.view', kwargs={"id":petition.id}))
