import unittest
from parser import parse_game
import pymongo


def get_sample_html():
    sample = "samples/game_153.html"
    with open(sample, "r") as myfile:
        html = myfile.read().replace('\n', '')
    return html


class MyTestCase(unittest.TestCase):

    def test_qa_tab(self):
        """Test mongo qa table."""
        qa_tab = pymongo.MongoClient().quest.qas
        test_qa = {'game_id': 0, 'question': "Up is cool.", 'answer': "Yup"}
        # Insert
        qa_tab.insert(test_qa)
        # Get it back
        qa = qa_tab.find_one(test_qa)
        print "Inserted and re-queried: ", qa
        self.assertEqual(test_qa['game_id'], qa['game_id'])
        self.assertEqual(test_qa['question'], qa['question'])
        self.assertEqual(test_qa['answer'], qa['answer'])

    def test_raw_tab(self):
        """Test mongo raw table."""
        raw_tab = pymongo.MongoClient().quest.raws
        test_raw = {'game_id': 0, 'html': get_sample_html()}
        # Insert
        raw_tab.insert(test_raw)
        # Get it back
        raw = raw_tab.find_one(test_raw)
        print "Inserted and re-queried html of length", len(raw['html'])
        self.assertEqual(test_raw['game_id'], raw['game_id'])
        self.assertEqual(test_raw['html'], raw['html'])

    def test_sample_game(self):
        """Parse the local sample game."""
        qa_dict = parse_game(get_sample_html())
        print "%s questions and answers found." % len(qa_dict)
        self.assertEqual(len(qa_dict), 48)
        # import pprint
        # pprint.pprint(qa_dict)

    # def test_something(self):
    #
    #     for game_id in parse_seasons(1):
    #         print parse_game(get_page(game_id))
    #
    #     self.assertEqual(True, False)


# class DbTestCase(unittest.TestCase):
#
#     def test_mongo(self):
#         test_data = dict(name='scott', animal='owl')
#         client = pymongo.MongoClient()
#         db = client.quest
#         posts = db.posts
#         post_id = posts.insert(test_data)
#         print post_id
#         val = posts.find_one()
#         print val







if __name__ == '__main__':
    unittest.main()
