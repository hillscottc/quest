import json
from questapp.models import Clue, DbStore


def load_clues(infile):
    with open(infile) as json_file:
        json_data = json.load(json_file)
        for clue_data in json_data:
            clue = Clue(**clue_data)
            clue.save()
    print "Clue count: {:,}".format(Clue.objects.count())


def dbstore_get(dbkey):
    return DbStore.objects.get(dbkey=dbkey).dbval


