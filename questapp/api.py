from questapp.models import Clue
from questapp.cors_base import CORSModelResource

# Note: API_LIMIT_PER_PAGE is set in settings/base.py


class ClueResource(CORSModelResource):
    class Meta:
        queryset = Clue.objects.all()
        resource_name = 'clue'


class RandomCluesResource(CORSModelResource):

    class Meta:
        queryset = Clue.objects.all().order_by('?')[:100]
        resource_name = 'random_clues'
