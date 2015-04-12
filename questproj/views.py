from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django import forms
from registration.backends.simple.views import RegistrationView

from questproj.forms import UserProfileForm, UserForm
from questapp.models import Clue
from questapp.utils import dbstore_get


def google_verify(request):
    return render(request, 'googlefd8980378f4a07d2.html')


class AdminPageForm(forms.Form):
    clue_source_name = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    answer_tracking = forms.BooleanField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))


class AdminPageFormView(View):
    form_class = AdminPageForm
    template_name = 'admin-page.html'

    def get(self, request, *args, **kwargs):
        initial = {'clue_source_name': dbstore_get('clue_source_name', "Jeopardy Clues"),
                   'answer_tracking': dbstore_get('answer_tracking', True)}
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


# Successful registration sends you to index page
class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/'

