import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from notification import models as notification
import forms

def index(request, page=0):
    all_news = models.Post.objects.all().filter(published=True)
    paginator = Paginator(all_news, 25)
    try: 
        items = paginator.page(page)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render_to_response('news/index.html', {'items':items}, context_instance = RequestContext(request))

def view(request, slug):
    item = models.Post.objects.get(slug__exact=slug)
    form = forms.CommentForm()
    return render_to_response('news/view.html', {'commentForm': form, 'item':item}, context_instance = RequestContext(request))

@login_required
def comment(request, id=None, parent=None):
    form = forms.CommentForm(request.POST)
    if form.is_valid():
        c = models.Comment()
        c.author = request.user
        c.body = form.cleaned_data['body']
        if parent:
            parentPost = models.Comment.objects.get(id__exact=parent)
            c.parent = parentPost
            notification.send([parentPost.author], "news_comment_reply", {"comment": c})
        elif id:
            newsPost = models.Post.objects.get(id__exact=id)
            c.post = newsPost
        c.save()
        return HttpResponseRedirect(reverse('news.views.view', kwargs={'slug': c.news_post().slug})+"#c"+str(c.id))

