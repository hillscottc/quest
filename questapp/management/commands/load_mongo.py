from django.core.management.base import BaseCommand
from pymongo import MongoClient
from questapp.models import Clue


class Command(BaseCommand):
    """ Inits the mongo questdb with random clues from the default db.
    """
    args = '<num>'
    help = 'Inits the mongo questdb with <num> random clues from the default db'
    default_num = 1000

    def handle(self, *args, **options):
        num = args[0] if args else self.default_num

        client = MongoClient()
        mongo_db = client.trivnode

        mongo_db.clues.drop()

        # for clue in Clue.objects.all().order_by('?')[:num]:
        for clue in Clue.objects.all():
            mongo_db.clues.insert({'question': clue.question,
                                   'answer': clue.answer,
                                   'category': clue.category})

        print "Mongo records:", mongo_db.clues.count()


