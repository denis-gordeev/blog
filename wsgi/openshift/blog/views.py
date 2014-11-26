from blog.models import BlogPost
from django.views.decorators.csrf import csrf_protect
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

def tagpage(request,tag):
    posts = BlogPost.objects.filter(tags__name=tag)
    return render_to_response('tagpage.html',{"posts":posts, "tag":tag})

@csrf_protect
def chat(request):
    '''
    main view
    '''
    print 'chat'
    c = {}
    messages = []
    if request.method == "POST":
        post = request.POST['message']
        return HttpResponse(parse(post))
    elif request.method == "GET":
        print 'lol get'
        return render_to_response("chat.html", {},
                               context_instance=RequestContext(request))
