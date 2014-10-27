from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext
from django.views.generic import ListView, DetailView, FormView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserProfileForm, UserForm


BASE_CONTEXT = {
    'SITE_NAME': settings.SITE_NAME,
}


def base_context(request):
    """The project's func-based home view needs this available in this way."""
    return BASE_CONTEXT


def home(request):
    """The project's home view."""
    context = RequestContext(request, processors=[base_context])
    return render(request, 'home.html', context_instance=context)


class BaseDetailView(DetailView):
    class Meta:  # pylint: disable=C0111,R0903
        abstract = True

    def get_context_data(self, *args, **kwargs):
        context = super(BaseDetailView, self).get_context_data(*args, **kwargs)
        context.update(BASE_CONTEXT)
        return context


class BaseTemplateView(TemplateView):
    class Meta:  # pylint: disable=C0111,R0903
        abstract = True

    def get_context_data(self, *args, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(*args, **kwargs)
        context.update(BASE_CONTEXT)

        return context


class BaseListView(ListView):
    class Meta:  # pylint: disable=C0111,R0903
        abstract = True

    def get_context_data(self, *args, **kwargs):
        context = super(BaseListView, self).get_context_data(*args, **kwargs)
        context.update(BASE_CONTEXT)

        return context


class BaseFormView(FormView):
    class Meta:  # pylint: disable=C0111,R0903
        abstract = True

    def get_context_data(self, *args, **kwargs):
        context = super(BaseFormView, self).get_context_data(*args, **kwargs)
        context.update(BASE_CONTEXT)

        return context


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

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
            #
            # # # Did the user provide a profile picture?
            # # # If so, we need to get it from the input form and put it in the UserProfile model.
            # # if 'picture' in request.FILES:
            # # profile.picture = request.FILES['picture']
            #
            # # Now we save the UserProfile model instance.
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
        'registration/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('registration/login.html', {}, context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# @login_required
# def user_account(request):
#     return render(request, 'registration/user_account.html', {})