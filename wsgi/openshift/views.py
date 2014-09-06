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

@csrf_protect
def chat(request):
    '''
    main view
    '''
    print 'lol'
    c = {}
    messages = []
    if request.method == "POST":
        print 'lol2'
        post = request.POST['message']
        return HttpResponse(parse(post))
    elif request.method == "GET":
        print 'lol get'
        return render_to_response("chat.html", {},
                               context_instance=RequestContext(request))


