from tastypie.resources import ModelResource
from tastypie import fields
from questapp.models import Clue
from tastypie.paginator import Paginator

from questproj.utils import get_random_ids


class ClueResource(ModelResource):
    class Meta:
        queryset = Clue.objects.all()
        resource_name = 'clue'
        paginator_class = Paginator


class RandomCluesResource(ModelResource):

    class Meta:
        queryset = Clue.objects.all().order_by('?')[:100]
        resource_name = 'random_clues'
