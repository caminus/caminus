import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request, page=0):
    all_news = models.Post.objects.all()
    paginator = Paginator(all_news, 25)
    try: 
        items = paginator.page(page)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render_to_response('news/index.html', {'items':items}, context_instance = RequestContext(request))

def view(request, slug):
    item = models.Post.objects.get(slug__exact=slug)
    return render_to_response('news/view.html', {'item':item}, context_instance = RequestContext(request))
