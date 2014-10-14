from django.test import TestCase
from questapp.models import get_relevant_counts
from questapp.utils import load_samples


class LoadSamplesTest(TestCase):

    def test_load_samples(self):
        """Loads some html sample files."""
        load_samples(100)
        counts = get_relevant_counts()
        print 'Counts:', counts
