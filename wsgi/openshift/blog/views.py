from blog.models import BlogPost
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from blog.forms import AddCommentaryForm, SearchForm

def tagpage(request,tag):
    posts = BlogPost.objects.filter(tags__name=tag)
    return render_to_response('tagpage.html',{"posts":posts, "tag":tag})

class PostList(ListView):
    template_name = 'blog.html'
    model = BlogPost

class PostDetails(TemplateView):
    template_name = 'post.html'
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
    # Overriding
    def get_context_data(self, **kwargs):
        context = super(PostDetails, self).get_context_data(**kwargs)
        post = self.get_post(kwargs['pk'])
        form = self.get_form(post)
        context.update({'form':form, 'post':post})
        return context

  # Helper
    def get_post(self, pk):
        return BlogPost.objects.get(pk=pk)

  # Helper
    def get_form(self, post):
        if self.request.method == 'POST':
            form = AddCommentaryForm(self.request.POST)
            if form.is_valid():
                commentary = form.save(commit=False)
                post.commentary_set.add(commentary)
            else:
                return form

        return AddCommentaryForm()
class SearchResults(ListView):
    print 'search'
    template_name = "searchresults.html"
    # Override
    def get_queryset(self):
        from django.db.models import Q
        if self.request.method == 'GET':
            form = SearchForm(self.request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                words = query.split(' ')
                qobjects = [Q(body__icontains=w) | Q(title__icontains=w) for w in words]
                condition = reduce(lambda x,y: x & y, qobjects)
                results = BlogPost.objects.filter(condition)
                return results
        return BlogPost.objects.none()
