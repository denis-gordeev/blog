import os
from parse import parse
from django.shortcuts import redirect
from django.core.context_processors import csrf
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.http import HttpResponse


def home(request):
    if request.method == "GET":
        return redirect('/blog/')
    if request.is_ajax():
        search = request.POST['search']
        print 'lolsearch'
        if search.length() > 0:
            posts = BlogPost.objects.all()
            for post in posts:
                if post.title.startswith(search):
                    result = post.title
        return HttpResponse(result)

@csrf_protect
def chat(request):
    '''
    main view
    '''
    print 'lol'
    c = {}
    messages = []
    if request.method == "POST":
        post = request.POST['message']
        return HttpResponse(parse(post))
    elif request.method == "GET":
        return render_to_response("chat.html", {},
                               context_instance=RequestContext(request))




