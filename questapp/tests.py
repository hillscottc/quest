import os
from django.test import TestCase
from django.test.utils import override_settings
from unittest import skip

from .models import Clue, Game
from .game_mgr import (TEST_GAME_ID, load_all_games, get_sample_ids, get_local_html,
                       get_fname, parse_game_html)

## Djangp TestCases force DEBUG=False, ignoring the settings file.
## Can override with @override_settings(DEBUG=True). To see django.db logging, for example.

class SamplesTest(TestCase):

    def test_samples(self):
        print
        parsed_ids, failed_ids = load_all_games()
        print "Games parsed:", len(parsed_ids), ", failed:", len(failed_ids)
        self.assertTrue(len(failed_ids) == 0)

        games = Game.objects.all()
        print "Loaded games to db:", len(games)
        self.assertGreater(len(games), 100)

        clues = Clue.objects.all()
        print "Loaded clues to db:", len(clues)
        self.assertGreater(len(clues), 7000)

        num_cats = len(set([clue.category for clue in clues]))
        print "Categories  :", num_cats
        self.assertGreater(num_cats, 900)


class UnitTest(TestCase):

    def setUp(self):
        print

    def test_get_sample_ids(self):
        """Get list of game_ids from samples.
        """
        game_ids = list(get_sample_ids())
        self.assertGreater(len(game_ids), 10)

    def test_get_local(self):
        """Open local test game file.
        """
        html = get_local_html(TEST_GAME_ID)
        length = len(html) if html else 0
        self.assertGreater(length, 3000)

    def test_get_fname(self):
        """Create file name for given id.
        """
        fname = get_fname(TEST_GAME_ID)
        self.assertIsNotNone(fname)
        self.assertTrue(os.path.isfile(fname))

    @override_settings(DEBUG=True)
    def test_save_clues(self):
        """Parse the test game, save to db.
        """
        html = get_local_html(TEST_GAME_ID)
        game = parse_game_html(html, TEST_GAME_ID)
        game.save()

        print game.desc()

        # clues = game.clue_set.all()
        # self.assertEqual(len(clues), 50)
        # print "First five clues in game {}:".format(TEST_GAME_ID)
        # for clue in game.clue_set.all():
        #     print clue

