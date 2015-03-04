import json
from django.core.management.base import BaseCommand
from questapp.models import Clue


class Command(BaseCommand):
    args = '<outfile>'
    help = 'Writes a json format dump file of the Clues.'

    def handle(self, *args, **options):
        if not args:
            raise ValueError("Output file arg not specified.")
        outfile = args[0]

        clue_qs = Clue.objects.all()
        clue_data = [{'question': clue.question, 'category': clue.category, 'answer': clue.answer}
                     for clue in clue_qs]

        with open(outfile, 'w') as out:
            json.dump(clue_data, out)

