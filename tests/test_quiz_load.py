from django.test import TestCase
from quizapp.utils import load_all


class TestQuizLoad(TestCase):

    def test_load(self):
        """Loads some html sample files."""
        load_all()


