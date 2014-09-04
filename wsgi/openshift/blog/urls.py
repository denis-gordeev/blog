from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from blog.models import BlogPost
from django.contrib.syndication.views import Feed

class BlogFeed(Feed):
    title = "Of men and crocodiles"
    link = "/blog/feed/"

    def items(self):
        return BlogPost.objects.all().order_by("-created")[:10]
    def item_title(self, item):
        return item.title
    def item_body(self, item):
        return item.body
    def item_link(self,item):
        return u"/blog/%d" % item.id


urlpatterns = patterns('blog.views',
    url(r'^$', ListView.as_view(
        queryset=BlogPost.objects.all().order_by("-created")[:10],
        template_name='blog.html')),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(
        model=BlogPost,
        template_name='post.html')),
    url(r'^archives/$', ListView.as_view(
        queryset=BlogPost.objects.all().order_by("-created"),
        template_name='archives.html')),
    url(r'^tag/(?P<tag>\w+)/$', 'tagpage'),
    url(r'^feed/$', BlogFeed())
)
