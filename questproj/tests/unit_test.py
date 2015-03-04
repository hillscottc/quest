from django.test import TestCase
from questapp.utils import load_clues
from questapp.models import Clue


class TestLoad(TestCase):
    def test_load_clues(self):
        """Load clues json file.
        """
        infile = 'questproj/fixtures/clues.json'
        load_clues(infile)
        count = Clue.objects.count()
        self.assertGreater(count, 5)



