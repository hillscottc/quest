from django.test import TestCase
from questapp.jeap_src_utils import load_samples
from questapp.models import get_relevant_counts


class LoadSamplesTest(TestCase):

    def test_load_samples(self):
        """Loads some samples."""
        load_samples(500)
        counts = get_relevant_counts()
        print 'Counts:', counts
