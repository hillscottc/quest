import os
from unittest import skip
from django.test.utils import override_settings
from django.test import TestCase
from questapp.models import Clue, Game
from questapp.parser import parse_game_html
from questapp.utils import (TEST_GAME_ID, TEST_SHOW_NUM, read_local_html, get_fname)
from questapp.utils import load_samples


class UnitTest(TestCase):

    def test_read_local(self):
        """Open local test game file."""
        html = read_local_html(TEST_GAME_ID)
        length = len(html) if html else 0
        self.assertGreater(length, 3000)

    def test_get_fname(self):
        """Create file name for given id."""
        fname = get_fname(TEST_GAME_ID)
        self.assertIsNotNone(fname)
        self.assertTrue(os.path.isfile(fname))

    @override_settings(DEBUG=True)
    def test_parse_game(self):
        """Parse the test game, save to db.
        Debug settings overrided.
        """
        html = read_local_html(TEST_GAME_ID)
        game, clues, errors = parse_game_html(html, TEST_GAME_ID)
        print game
        self.assertEqual(game.gid, TEST_GAME_ID)
        self.assertEqual(game.sid, str(TEST_SHOW_NUM))
        # clues = game.clue_set.all()
        # self.assertEqual(len(clues), 48)
        # print "First five clues in game {}:".format(TEST_GAME_ID)
        # for clue in game.clue_set.all()[:5]:
        #     print clue,
        # print


# @skip('Skip the load all tests.')
class TestLoad(TestCase):
    def test_load_samples(self):
        """Load some jeapordy html game files."""
        num_files = None
        load_samples(num_files)
        # self.assertEqual(Game.objects.count(), num_files)



