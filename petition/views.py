import models
import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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
        return HttpResponseRedirect(reverse('petition.views.view', kwargs={"id":petition.id}))
    return render_to_response('petition/create.html', {'form':form}, context_instance = RequestContext(request))

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
        return HttpResponseRedirect(reverse('petition.views.view', kwargs={"id":petition.id})+"#c"+str(comment.id))
