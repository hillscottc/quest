import unittest
from soup_jeap import parse_seasons, parse_game, get_page


class MyTestCase(unittest.TestCase):

    def test_something(self):

        for game_id in parse_seasons(1):
            print parse_game(get_page(game_id))

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
