from django.core.management.base import NoArgsCommand
from questapp.models import Clue
from django.core import serializers

OUTFILE = 'clues.json'


class Command(NoArgsCommand):
    help = 'Parese and load all the html files.'

    def handle_noargs(self, **options):
        json_serializer = serializers.get_serializer("json")()
        with open(OUTFILE, "w") as out:
            json_serializer.serialize(Clue.objects.all()[:10],
                                      fields=('question', 'category', 'answer'),
                                      stream=out)
