import random
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, FormView
from django.views.generic import TemplateView
from .models import Clue, Category
from .forms import ClueSearchForm
import questproj.cache_mgr as cache_mgr


class HomeView(TemplateView):
    template_name = "questapp_home.html"


class ClueDetailView(DetailView):
    context_object_name = 'clue'
    queryset = Clue.objects.all()
    template_name = "clue_detail.html"

    def get_object(self, *args, **kwargs):
        object = super(ClueDetailView, self).get_object(*args, **kwargs)
        # Record the last accessed date
        object.last_accessed = timezone.now()
        object.save()
        return object


class ClueListView(ListView):
    context_object_name = 'clue_list'
    template_name = 'clue_list.html'
    queryset = Clue.objects.all()


class ClueRandomView(ListView):
    context_object_name = 'clue_list'
    template_name = 'clue_list.html'
    num_returned = 15

    def get_context_data(self, **kwargs):
        context = super(ClueRandomView, self).get_context_data(**kwargs)
        context.update({'page_subtitle': 'Some Random Clues'})
        context.update({'list_type': 'clues-list'})
        return context

    def get_queryset(self):
        clue_list = cache_mgr.get_cached_objs(Clue, self.num_returned)
        return clue_list


class CatRandomView(ListView):
    context_object_name = 'cat_list'
    template_name = 'cat_list.html'
    num_returned = 15

    def get_context_data(self, **kwargs):
        context = super(CatRandomView, self).get_context_data(**kwargs)
        context.update({'page_subtitle': 'Some Random Categories'})
        context.update({'list_type': 'cat-list'})
        return context

    def get_queryset(self):
        cat_list = cache_mgr.get_cached_objs(Category, self.num_returned)
        return cat_list


class CluesByCatView(ListView):
    context_object_name = 'clue_list'
    template_name = 'clue_list.html'

    def get_context_data(self, *args, **kwargs):

        cat_id = int(float(self.kwargs['cat_id']))
        cat = Category.objects.get(id=cat_id)

        context = super(CluesByCatView, self).get_context_data(*args, **kwargs)
        context.update({'list_type': 'clues-by-cat'})
        context.update({'page_subtitle': 'Clues by Category, %s' % cat.name})
        context.update({'cat': cat})
        return context

    def get_queryset(self):
        cat_id = int(float(self.kwargs['cat_id']))
        cat = Category.objects.get(id=cat_id)
        qs = Clue.objects.filter(category__name=cat.name)
        return qs.all()


class CatListView(ListView):
    context_object_name = 'cat_list'
    template_name = 'cat_list.html'

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset


class ClueSearchView(FormView):
    template_name = "clue_search.html"
    form_class = ClueSearchForm

    def form_valid(self, form):
        cd = form.cleaned_data
        context = self.get_context_data(form=form)

        if not cd['search_txt']:
            msg = "All recs."
            qs = Clue.objects.all()
        else:
            msg = "Searching by: " + cd['search_txt']
            qs = Clue.objects.filter(question__contains=cd['search_txt'])

        max_recs = 50
        clue_list = qs[:max_recs]

        context.update({'test_msg': msg})
        context.update({'list_type': 'clues-search'})
        context.update({'clue_list': clue_list})
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('clue-search')