from tastypie.resources import ModelResource
from tastypie import fields
from questapp.models import Clue, Category
import questproj.cache_mgr as cache_mgr
from questproj.utils import get_random_ids


class CategoryResource(ModelResource):

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'


class ClueResource(ModelResource):
    category = fields.ToOneField(CategoryResource, 'category', full=True)

    class Meta:
        queryset = Clue.objects.all()
        resource_name = 'clue'


class RandomCluesResource(ModelResource):
    category = fields.ToOneField(CategoryResource, 'category', full=True)

    class Meta:
        rand_ids = get_random_ids(Clue, 1000)
        queryset = Clue.objects.filter(id__in=rand_ids)
        resource_name = 'random_clues'