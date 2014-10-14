from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Clue, Category
from django.conf import settings
from questproj.utils import get_random_objs


class HomeView(TemplateView):
    template_name = "home.html"


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