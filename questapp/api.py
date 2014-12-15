from tastypie.resources import ModelResource
from tastypie import fields
from questapp.models import Clue, Category


class CategoryResource(ModelResource):

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'


class ClueResource(ModelResource):
    category = fields.ToOneField(CategoryResource, 'category', full=True)

    class Meta:
        queryset = Clue.objects.all()
        resource_name = 'clue'
