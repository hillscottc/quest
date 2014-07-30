import os
from django.test import TestCase

from questapp.models import Clue
from questapp.parser import parse_game
from questapp.utils import get_local_game, get_game_fname


TEST_GAME_ID = 4529


class ParserTest(TestCase):

    def test_parse_game(self):
        """Parse a game."""
        html = get_local_game(TEST_GAME_ID)
        clues = list(parse_game(html))
        print "Clues parsed from test game:", len(clues)
        self.assertEqual(len(clues), 50)

    def test_get_local_games(self):
        """Test opening local game files."""
        for game_id in [TEST_GAME_ID, 84]:
            html = get_local_game(game_id)
            length = len(html) if html else 0
            print "Game id", game_id, "length", length
            self.assertGreater(length, 3000)

    def test_get_game_fname(self):
        """Create file name for given id."""
        fname = get_game_fname(TEST_GAME_ID)
        self.assertIsNotNone(fname)
        self.assertTrue(os.path.isfile(fname))


class DbTest(TestCase):

    def test_clues(self):
        """Test db read and write of clues."""
        print "Get test game html."
        html = get_local_game(TEST_GAME_ID)
        print "Parse game, write clues to db."
        for clue in list(parse_game(html)):
            clue.save()

        print "Verify count of test game records."
        count = Clue.objects.count()
        self.assertEqual(count, 50)

