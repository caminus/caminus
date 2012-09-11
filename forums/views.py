import models
import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from notification import models as notification
from api.events import server_broadcast, user_broadcast

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
        if reply.parent.user !=  request.user:
            notification.send([reply.parent.user], "forum_reply", {"reply": reply, 'notice_url': reverse('forums.views.post', kwargs={'id':reply.id}), 'notice_description': reply.topic().title})
        messages.info(request, "Reply successful")
        user_message(reply.parent.user, "%s replied to your post in '%s'",
            request.user, reply.topic().title)
        return HttpResponseRedirect(reverse('forums.views.post', kwargs={"id":reply.id}))
    return render_to_response('forums/reply.html', {"parent":parentPost, "form":form}, context_instance = RequestContext(request))

@login_required
def newTopic(request, forumID=None):
    parentForum = models.Forum.objects.get(id__exact=forumID)
    permitted = False
    postingRights = parentForum.acls.all()
    if len(postingRights) == 0:
        permitted = True
    for group in request.user.groups.all():
        if permitted:
            break
        for acl in postingRights:
            if group == acl.group:
                permitted = True
                break
    if not permitted:
        messages.error(request, "You are not permitted to post in this forum.")
        return HttpResponseRedirect(parentForum.get_absolute_url())
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
        messages.info(request, "Posting successful")
        server_broadcast("New forum topic: %s", topic.title)
        return HttpResponseRedirect(reverse('forums.views.post', kwargs={'id': reply.id}))
    return render_to_response('forums/newTopic.html', {"forum":parentForum, "replyForm":replyForm, "topicForm": topicForm}, context_instance = RequestContext(request))

@login_required
def editPost(request, postID=None):
    post = models.Post.objects.get(id__exact=postID)
    if post.user != request.user and not request.user.has_perm('edit_posts'):
      raise PermissionDenied
    if request.method == 'POST':
        form = forms.ReplyForm(request.POST)
    else:
        form = forms.ReplyForm(instance=post)
    
    if form.is_valid():
        post.body = form.cleaned_data['body']
        post.save()
        messages.info(request, "Post updated.")
        return HttpResponseRedirect(reverse('forums.views.post',
          kwargs={"id":post.id}))
    return render_to_response('forums/edit.html', {"post": post, "parent":
      post.parent, "form": form}, context_instance = RequestContext(request))

@permission_required('forums.delete_topic')
def deleteTopic(request, topicID):
    topic = models.Topic.objects.get(id__exact=topicID)
    forumID = topic.forum.slug
    topic.delete()
    messages.info(request, "Thread deleted.")
    return HttpResponseRedirect(reverse('forums.views.forum', kwargs={'forum': forumID}))

@permission_required('forums.sticky_topic')
def stickyTopic(request, topicID):
    topic = models.Topic.objects.get(id__exact=topicID)
    topic.sticky = (not topic.sticky)
    topic.save()
    if topic.sticky:
        messages.info(request, "Topic is now sticky")
    else:
        messages.info(request, "Topic is no longer sticky")
    return HttpResponseRedirect(reverse('forums.views.topic', kwargs={'topicID': topic.id}))

@csrf_exempt
def preview(request):
    reply = models.Post(body=request.POST['body'], user=request.user)
    return render_to_response('forums/_reply.html', {'post': reply}, context_instance = RequestContext(request))
