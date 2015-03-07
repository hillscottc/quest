from django.test import TestCase
from questapp.utils import load_clues
from questapp.models import Clue, DbStore
from questapp.utils import dbstore_get

class UnitTest(TestCase):
    def test_dbstore(self):
        test_key = "color"
        test_val = "blue"
        DbStore.objects.create(dbkey=test_key, dbval=test_val)
        result = dbstore_get(test_key)
        print "Got ", result
        self.assertEqual(test_val, result)


# class TestLoad(TestCase):
#     def test_load_clues(self):
#         """Load clues json file.
#         """
#         infile = 'questproj/fixtures/clues.json'
#         load_clues(infile)
#         count = Clue.objects.count()
#         self.assertGreater(count, 5)





