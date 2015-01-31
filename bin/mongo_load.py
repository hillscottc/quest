from pymongo import MongoClient
from questapp.models import Clue


def load_mongo():
    client = MongoClient()
    db = client.quest_db

    db.clues.drop()

    for pg_clue in Clue.objects.all()[:1000]:
        db.clues.insert({'question': pg_clue.question,
                         'answer': pg_clue.answer,
                         'category': pg_clue.category})

    print [clue for clue in db.clues.find()]


