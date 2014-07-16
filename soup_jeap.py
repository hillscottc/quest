import requests
import re
from pprint import pprint
from string import split
from bs4 import BeautifulSoup
import pymongo


def get_soup():
    # r = requests.get('http://www.j-archive.com/showgame.php?game_id=4529')
    # return BeautifulSoup(r.text)
    return BeautifulSoup(open("soup_jeap_sample.html"))


def parse_seasons():
    # ids = range(30)
    ids = range(1)

    for seas_id in ids:
        url = 'http://www.j-archive.com/showseason.php?season=' + str(seas_id + 1)
        print 'Getting', url
        soup = BeautifulSoup(requests.get(url).text)
        print [l['href'] for l in soup.find_all('a') if 'game_id' in l['href']]


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


def qa_dict():
    qa_dict = {}
    for div_tag in get_soup().find_all('div'):
        question, answer = parse_qa_from_div(div_tag)       
        if question and answer:
            qa_dict[question] = answer
    return qa_dict


if __name__ == '__main__':
    # pprint(qa_dict())
    # parse_seasons()

    test_data = dict(name='scott', animal='owl')

    client = pymongo.MongoClient()
    db = client.quest
    posts = db.posts
    posts.insert(test_data)
    posts.find_one()







