from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView, TemplateView
from views import chat
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blog.views import SearchResults, register,user_login, user_logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'openshift.views.home', name='home'),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chat/$', chat, name='chat'),
    url(r'^search/', SearchResults.as_view(), name="search"),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^accounts/', include('allauth.urls')),
)

urlpatterns += staticfiles_urlpatterns()
