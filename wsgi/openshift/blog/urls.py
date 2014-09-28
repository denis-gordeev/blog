from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView, TemplateView
from blog.models import BlogPost
from django.contrib.syndication.views import Feed
from views import chat

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
        queryset=BlogPost.objects.all().order_by("-created"),
        template_name='blog.html')),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(
        model=BlogPost,
        template_name='post.html')),
    url(r'^archives/$', ListView.as_view(
        queryset=BlogPost.objects.all().order_by("-created"),
        template_name='archives.html')),
    url(r'^tag/(?P<tag>\w+)/$', 'tagpage'),
    url(r'^feed/$', BlogFeed()),
    url(r'^links$', TemplateView.as_view(template_name='links.html'), name="links"),
    url(r'^contacts$', TemplateView.as_view(template_name='contacts.html'), name="contacts"),
    url(r'^solutions$', ListView.as_view(
        queryset=BlogPost.objects.filter(tags__name='solutions').order_by("-created"),
        template_name='blog.html')),
)
