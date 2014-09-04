from blog.models import BlogPost
from django.shortcuts import render_to_response

def tagpage(request,tag):
    posts = BlogPost.objects.filter(tags__name=tag)
    return render_to_response('tagpage.html',{"posts":posts, "tag":tag})
