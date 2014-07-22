import requests
import re
from string import split
from bs4 import BeautifulSoup


def parse_game(page):
    bs = BeautifulSoup(page)
    qa_dict = {}

    cats = []
    for td_tag in bs.find_all('td'):
        if td_tag.get('class') == ['category_name']:
            cats.append(td_tag.text)
    print "Must add these cats somehow"
    print cats

    for div_tag in bs.find_all('div'):
        question, answer = parse_qa_from_div(div_tag)
        if question and answer:
            qa_dict[question] = answer

    return qa_dict


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
