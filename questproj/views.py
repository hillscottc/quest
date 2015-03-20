from datetime import date
from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.template import RequestContext
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django import forms
from questproj.forms import UserProfileForm, UserForm
from questapp.models import Clue, UserLog
from questapp.utils import dbstore_get


def google_verify(request):
    return render(request, 'googlefd8980378f4a07d2.html')


def get_counts(user):
    counts = {}
    if user.username:
        counts['user_today'] = UserLog.objects.filter(created__gte=date.today(),
                                                      userid=user.id).count()
        counts['user_alltime'] = UserLog.objects.filter(userid=user.id).count()
    else:
        counts['user_today'] = '-'
        counts['user_alltime'] = '-'

    counts['everyone_today'] = UserLog.objects.filter(created__gte=date.today()).count()
    counts['everyone_alltime'] = UserLog.objects.count()
    return counts


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'api_limit': settings.API_LIMIT_PER_PAGE})
        context.update(get_counts(self.request.user))
        return context


class HomeView(TemplateView):
    template_name = "home.html"

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     context.update({'clue_source_name': settings.CLUE_SOURCE_NAME})
    #     return context


class AdminPageForm(forms.Form):
    clue_source_name = forms.CharField(max_length=12)


class AdminPageFormView(View):
    form_class = AdminPageForm
    template_name = 'admin-page.html'

    def get(self, request, *args, **kwargs):
        try:
            clue_source_name = dbstore_get('clue_source_name')
        except ObjectDoesNotExist:
            clue_source_name = "Jeopardy Clues"

        initial = {'clue_source_name': clue_source_name}

        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            # return HttpResponseRedirect('/success/')
            pass

        return render(request, self.template_name, {'form': form})


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context.update({'clue_count': Clue.objects.count()})
        return context


class TestMariView(TemplateView):
    template_name = "test-mari.html"


class UserAccountView(TemplateView):
    template_name = "registration/user_account.html"


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
    return HttpResponseRedirect(reverse('home'))


# @login_required
# def user_account(request):
#     return render(request, 'registration/user_account.html', {})