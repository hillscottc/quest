from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import Category


class AboutView(TemplateView):
    template_name = "about.html"


class CategoryListView(ListView):
    model = Category

    # def head(self, *args, **kwargs):
    #     last_book = self.get_queryset().latest('publication_date')
    #     response = HttpResponse('')
    #     # RFC 1123 date format
    #     response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
    #     return response