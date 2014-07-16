import requests
import re
from string import split
from bs4 import BeautifulSoup
import pymongo

URL_BASE = 'http://www.j-archive.com/showgame.php?game_id='


def db_get(game_id):
    print 'fake db get', game_id
    # return None


def db_save(game_id, page):
    print 'fake db save', game_id, page[:20], '...'
    # client = pymongo.MongoClient()
    # db = client.quest
    # return db.pages.insert(page)


def get_page(game_id):
    url = URL_BASE + game_id
    # Try to get page from db first
    page = db_get(game_id)
    if not page:
        page = requests.get(url).text
        db_save(game_id, page)
    return page


def parse_seasons(count=1):
    """Get game_ids from given number of seasons."""
    ids = range(count)
    game_ids = []
    for seas_id in ids:
        url = 'http://www.j-archive.com/showseason.php?season=' + str(seas_id + 1)
        print 'Getting', url
        soup = BeautifulSoup(requests.get(url).text)

        for tag in soup.find_all('a'):
            if 'game_id' in tag['href']:
                match = re.search('\d+', tag['href'])
                if match:
                    game_ids.append(match.group(0))
    return game_ids


def parse_qa_from_div(div_tag):

    question, answer = '', ''    
    regex_ans = '(.*)("correct_response">)([^<]+)'

    # Answer
    a_attr = div_tag.get('onmouseover')
    if a_attr:
        match = re.match(regex_ans, a_attr)
        if match:
            answer = match.group(3)
            
    # Question
    q_attr = div_tag.get('onmouseout')
    if q_attr:
        question = split(q_attr, ", '",  2)[2][:-2]
        
    return question, answer


def parse_game(page):
    bs = BeautifulSoup(page)
    qa_dict = {}
    # for div_tag in get_soup().find_all('div'):
    for div_tag in bs.find_all('div'):
        question, answer = parse_qa_from_div(div_tag)
        if question and answer:
            qa_dict[question] = answer
    return qa_dict


# def mongo_test():
#     test_data = dict(name='scott', animal='owl')
#     client = pymongo.MongoClient()
#     db = client.quest
#     posts = db.posts
#     post_id = posts.insert(test_data)
#     print post_id
#     val = posts.find_one()
#     print val
#


    # outfile = open('sids.out.txt', 'w')
    # for sid in sids:
    #     outfile.write(sid + '\n')
    # outfile.close()













