from questapp.models import Clue
from questapp.cors_base import CORSModelResource


class ClueResource(CORSModelResource):
    class Meta:
        queryset = Clue.objects.all()
        resource_name = 'clue'


class RandomCluesResource(CORSModelResource):

    class Meta:
        queryset = Clue.objects.all().order_by('?')[:100]
        resource_name = 'random_clues'
