import json
from django.conf import  settings
from questapp.models import Clue, DbStore
from django.core.exceptions import ObjectDoesNotExist

def load_clues(infile):
    with open(infile) as json_file:
        json_data = json.load(json_file)
        for clue_data in json_data:
            clue = Clue(**clue_data)
            clue.save()
    print "Clue count: {:,}".format(Clue.objects.count())


def dbstore_get(dbkey, default=None):
    try:
        return DbStore.objects.get(dbkey=dbkey).dbval
    except ObjectDoesNotExist:
        if not default:
            raise
        else:
            return default


def get_clue_source_name():
    try:
        return dbstore_get('clue_source_name')
    except ObjectDoesNotExist:
        return "Clues"


