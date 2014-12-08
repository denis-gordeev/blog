from blog.models import BlogPost, User
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, TemplateView
from blog.forms import AddCommentaryForm, SearchForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def tagpage(request,tag):
    posts = BlogPost.objects.filter(tags__name=tag)
    return render_to_response('tagpage.html',{"posts":posts, "tag":tag})

class PostList(ListView):
    template_name = 'blog.html'
    model = BlogPost

class PostDetails(TemplateView):
    def __init(self):
        self.current_user = 0
    template_name = 'post.html'
    def post(self, request, *args, **kwargs):
        self.current_user = request.user
        login_required = True
        kwargs['author'] = request.user
        return self.get(request, *args, **kwargs)
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
                commentary.author = self.current_user
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

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/blog/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is inactive.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/blog/')
