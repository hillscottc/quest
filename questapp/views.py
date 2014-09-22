from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Clue, Category


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


class ClueListView(ListView):
    context_object_name = 'clue_list'
    template_name = 'clue_list.html'
    queryset = Clue.objects.all()
    paginate_by = 10


class CatListView(ListView):
    context_object_name = 'cat_list'
    template_name = 'cat_list.html'
    queryset = Category.objects.all()
