from tastypie.resources import ModelResource
from tastypie import fields
from questapp.models import Clue
from tastypie.paginator import Paginator

from questproj.utils import get_random_ids


class ClueResource(ModelResource):
    class Meta:
        queryset = Clue.objects.all()
        resource_name = 'clue'


class RandomCluesResource(ModelResource):

    class Meta:
        rand_ids = get_random_ids(Clue, 1000)
        queryset = Clue.objects.filter(id__in=rand_ids)
        resource_name = 'random_clues'
        paginator_class = Paginator