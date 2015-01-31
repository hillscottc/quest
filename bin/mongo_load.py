from pymongo import MongoClient
from questapp.models import Clue


def load_mongo(num=1000):
    """ Inits the mongo questdb with random clues from the default db.
    """
    client = MongoClient()
    mongo_db = client.quest_db
    mongo_db.clues.drop()

    for clue in Clue.objects.all().order_by('?')[:num]:
        mongo_db.clues.insert({'question': clue.question,
                               'answer': clue.answer,
                               'category': clue.category})

    print "Mongo records:", mongo_db.clues.count()

