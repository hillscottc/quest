import datetime as dt
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, View
from django import forms
from django.db.models import Count
from registration.backends.simple.views import RegistrationView

from questapp.models import Clue, UserLog, CountCase
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


def get_counts(user):

    counts = {}

    if user.is_authenticated():

        rows = UserLog.get_counts_filtered({'userid': 1, 'created__gte': dt.date.today()})
        if rows:
            counts['user_today_right'] = rows[0]['is_correct_yes']
            counts['user_today_wrong'] = rows[0]['is_correct_no']
        else:
            counts['user_today_right'] = 0
            counts['user_today_wrong'] = 0

        rows = UserLog.get_counts_filtered({'userid': 1})
        if rows:
            counts['user_alltime_right'] = rows[0]['is_correct_yes']
            counts['user_alltime_wrong'] = rows[0]['is_correct_no']
        else:
            counts['user_alltime_right'] = 0
            counts['user_alltime_wrong'] = 0

    rows = UserLog.get_counts_filtered({'created__gte': dt.date.today()})
    if rows:
        counts['everyone_today_right'] = rows[0]['is_correct_yes']
        counts['everyone_today_wrong'] = rows[0]['is_correct_no']
    else:
        counts['everyone_today_right'] = 0
        counts['everyone_today_wrong'] = 0

    rows = UserLog.get_counts_filtered()
    if rows:
        counts['everyone_alltime_right'] = rows[0]['is_correct_yes']
        counts['everyone_alltime_wrong'] = rows[0]['is_correct_no']
    else:
        counts['everyone_alltime_right'] = 0
        counts['everyone_alltime_wrong'] = 0


    # counts['everyone_today_right'] = UserLog.objects.filter(
    #     correct=True, created__gte=dt.date.today()).count()
    # counts['everyone_today_wrong'] = UserLog.objects.filter(
    #     correct=False, created__gte=dt.date.today()).count()
    #
    # counts['everyone_alltime_right'] = UserLog.objects.filter(correct=True).count()
    # counts['everyone_alltime_wrong'] = UserLog.objects.filter(correct=False).count()

    # For the newer table.

    logs = UserLog.objects.values('userid').annotate(
        is_correct_yes=CountCase('correct', when=True),
        total=Count('userid'))
    for row in logs:
        row['percentage'] = 100 * (float(row['is_correct_yes']) / row['total'])

    counts['logs'] = logs
    return counts


class ScoreboardView(TemplateView):
    template_name = "scoreboard.html"



    def get_context_data(self, **kwargs):
        context = super(ScoreboardView, self).get_context_data(**kwargs)

        context.update(get_counts(self.request.user))

        return context


class UserAccountView(TemplateView):
    template_name = "registration/user_account.html"


# Successful registration sends you to index page
class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/'


