import json
from django.conf import  settings
from questapp.models import Clue, DbStore
from django.core.exceptions import ObjectDoesNotExist

def load_clues(infile, limit=10000):
    with open(infile) as json_file:
        json_data = json.load(json_file)
        for i, clue_data in enumerate(json_data):
            clue = Clue(**clue_data)
            clue.save()
            if i > limit:
                break
    print "Clue count: {:,}".format(Clue.objects.count())


def dbstore_get(dbkey, default):
    try:
        return DbStore.objects.get(dbkey=dbkey).dbval
    except ObjectDoesNotExist:
        return default


def get_clue_source_name():
    try:
        return dbstore_get('clue_source_name')
    except ObjectDoesNotExist:
        return "Clues"


