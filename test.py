import unittest
from parser import parse_game
from utils import get_local_game
import pymongo

TEST_GAME_ID = 4529


def get_sample_html():
    sample = "samples/game_4529.html"
    with open(sample, "r") as myfile:
        html = myfile.read().replace('\n', '')
    return html


class ParserUnitTest(unittest.TestCase):

    def test_parse_game(self):
        """Parse a game."""
        game = get_local_game(TEST_GAME_ID)
        clues = list(parse_game(game))
        # print clues
        print "Sample game has %s questions and answers." % len(clues)
        # self.assertEqual(len(clues), 48)

    def test_get_local_games(self):
        """Test opening local game files."""
        for game_id in [TEST_GAME_ID, 81, 82, 83, 84, 85]:
            html = get_local_game(game_id)
            length = len(html) if html else 0
            print "Game id", game_id, "length", length


# class DbTest(unittest.TestCase):
#
#     def test_write_clue(self):
#         with open(get_sample_html(), "r") as myfile:
#             html = myfile.read().replace('\n', '')
#         clue_list = parse_game(html)
#         coll = pymongo.MongoClient().quest.clues
#         for clue in clue_list:
#             coll.insert(clue)
#
#     def test_qa_tab(self):
#         """Test mongo qa table."""
#         qa_tab = pymongo.MongoClient().quest.qas
#         test_qa = {'game_id': 0, 'question': "Up is cool.", 'answer': "Yup"}
#         # Insert
#         qa_tab.insert(test_qa)
#         # Get it back
#         qa = qa_tab.find_one(test_qa)
#         print "Inserted and re-queried: ", qa
#         self.assertEqual(test_qa['game_id'], qa['game_id'])
#         self.assertEqual(test_qa['question'], qa['question'])
#         self.assertEqual(test_qa['answer'], qa['answer'])
#
#     def test_raw_tab(self):
#         """Test mongo raw table."""
#         raw_tab = pymongo.MongoClient().quest.raws
#         test_raw = {'game_id': 0, 'html': get_sample_html()}
#         # Insert
#         raw_tab.insert(test_raw)
#         # Get it back
#         raw = raw_tab.find_one(test_raw)
#         print "Inserted and re-queried html of length", len(raw['html'])
#         self.assertEqual(test_raw['game_id'], raw['game_id'])
#         self.assertEqual(test_raw['html'], raw['html'])



if __name__ == '__main__':
    unittest.main()
