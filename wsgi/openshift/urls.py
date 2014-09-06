from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView, TemplateView
from views import chat


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'openshift.views.home', name='home'),
    url(r'^blog/$', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chat/$', chat, name='chat'),
)

