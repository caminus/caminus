import models
import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from notification import models as notification

def index(request):
    forums = models.Forum.objects.filter(parent=None)
    return render_to_response('forums/index.html', {"forums":forums}, context_instance = RequestContext(request))

def forum(request, forum):
    forum = models.Forum.objects.get(slug=forum)
    topics = forum.topic_set.all()
    return render_to_response('forums/forum.html', {"forum":forum, "topics":topics}, context_instance = RequestContext(request))

def topic(request, topicID, forumSlug=None, topicSlug=None):
    topic = models.Topic.objects.get(id=topicID)
    return render_to_response('forums/topic.html', {"topic":topic}, context_instance = RequestContext(request))

def post(request, id):
    post = models.Post.objects.get(id=id)
    rootPost = post.get_root()
    return HttpResponseRedirect(reverse('forums.views.topic', kwargs={"topicID":rootPost.topic().id})+"#reply-"+id)

@login_required
def reply(request, topicID=None):
    parentPost = models.Post.objects.get(id__exact=topicID)
    if request.method == 'POST':
        form = forms.ReplyForm(request.POST)
    else:
        form = forms.ReplyForm()
    if form.is_valid():
        reply = models.Post()
        reply.parent = parentPost
        reply.body = form.cleaned_data['body']
        reply.user = request.user
        reply.save()
        notification.send([reply.parent.user], "forum_reply", {"reply": reply})
        return HttpResponseRedirect(reverse('forums.views.post', kwargs={"id":reply.id}))
    return render_to_response('forums/reply.html', {"post":parentPost, "form":form}, context_instance = RequestContext(request))

@login_required
def newTopic(request, forumID=None):
    parentForum = models.Forum.objects.get(id__exact=forumID)
    if request.method == 'POST':
        replyForm = forms.ReplyForm(request.POST, prefix='reply')
        topicForm = forms.TopicForm(request.POST, prefix='topic')
    else:
        replyForm = forms.ReplyForm(prefix='reply')
        topicForm = forms.TopicForm(prefix='topic')
    if replyForm.is_valid() and topicForm.is_valid():
        topic = models.Topic()
        topic.title = topicForm.cleaned_data['title']
        topic.forum = parentForum
        reply = models.Post()
        reply.body = replyForm.cleaned_data['body']
        reply.user = request.user
        reply.save()
        topic.rootPost = reply
        topic.save()
        return HttpResponseRedirect(reverse('forums.views.post', kwargs={'id': reply.id}))
    return render_to_response('forums/newTopic.html', {"forum":parentForum, "replyForm":replyForm, "topicForm": topicForm}, context_instance = RequestContext(request))
