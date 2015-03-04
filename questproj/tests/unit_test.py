import os
from unittest import skip
from django.test.utils import override_settings
from django.test import TestCase
from questapp.models import Clue
from questapp.utils import (TEST_GAME_ID, TEST_SHOW_NUM, read_local_html, get_fname)
from questapp.utils import load_samples


# @skip('Skip the load all tests.')
# class TestLoad(TestCase):
#     def test_load_samples(self):
#         """Load some jeapordy html game files."""
#         num_files = None
#         load_samples(num_files)
#         # self.assertEqual(Game.objects.count(), num_files)



