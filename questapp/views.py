from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from .models import Clue


class AboutView(TemplateView):
    template_name = "about.html"


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


# class ClueCreate(CreateView):
#     model = Clue
#     fields = ['category', 'question', 'answer']
#
#
# class ClueUpdate(UpdateView):
#     model = Clue
#     fields = ['category', 'question', 'answer']
#
#
# class ClueDelete(DeleteView):
#     model = Clue
#     success_url = reverse_lazy('clue-list')