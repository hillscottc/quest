from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, FormView
from django.utils import timezone
from django.core.urlresolvers import reverse
from .models import Clue, Category
from .forms import TestForm
from django.conf import settings
from questproj.utils import get_random_objs


class TestFormView(FormView):
    template_name = "test.html"
    form_class = TestForm

    def get_context_data(self, **kwargs):
        context = super(TestFormView, self).get_context_data(**kwargs)
        context['SITE_NAME'] = settings.SITE_NAME
        return context

    def form_valid(self, form):
        cd = form.cleaned_data
        msg = None
        if cd['test_txt']:
            msg = "You said " + cd['test_txt']

        context = self.get_context_data(form=form)
        if msg:
            context.update({'test_msg': msg})
        return self.render_to_response(context)
        # return super(TestFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('test-form')


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['SITE_NAME'] = settings.SITE_NAME
        return context


class ClueDetailView(DetailView):
    context_object_name = 'clue'
    queryset = Clue.objects.all()
    template_name = "clue_detail.html"

    def get_object(self):
        object = super(ClueDetailView, self).get_object()
        # Record the last accessed date
        object.last_accessed = timezone.now()
        object.save()
        return object

    def get_context_data(self, **kwargs):
        context = super(ClueDetailView, self).get_context_data(**kwargs)
        context['SITE_NAME'] = settings.SITE_NAME
        return context


class ClueListView(ListView):
    context_object_name = 'clue_list'
    template_name = 'clue_list.html'
    queryset = Clue.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ClueListView, self).get_context_data(**kwargs)
        context['SITE_NAME'] = settings.SITE_NAME
        return context


class ClueRandomView(ListView):
    context_object_name = 'clue_list'
    template_name = 'clue_list.html'

    def get_queryset(self):
        output = list(get_random_objs(Clue, int(float(self.kwargs['num']))))
        return output

    def get_context_data(self, **kwargs):
        context = super(ClueRandomView, self).get_context_data(**kwargs)
        context['SITE_NAME'] = settings.SITE_NAME
        return context


class CatListView(ListView):
    context_object_name = 'cat_list'
    template_name = 'cat_list.html'
    queryset = Category.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CatListView, self).get_context_data(**kwargs)
        context['SITE_NAME'] = settings.SITE_NAME
        return context