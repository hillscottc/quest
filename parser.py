import requests
import re
from string import split
from bs4 import BeautifulSoup


def parse_game(page):
    bs = BeautifulSoup(page)
    qa_dict = {}

    rounds = bs.find_all('table', {'class': 'round'})
    rounds = rounds + bs.find_all('table', {'class': 'final_round'})
    for game_round in rounds:
        cats = [t.text for t in game_round.find_all('td', {'class': 'category_name'})]
        print cats
        for div_tag in game_round.find_all('div'):
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


if __name__ == '__main__':
    sample = "samples/game_153.html"
    # with open(sample, "r") as myfile:
    #     html = myfile.read().replace('\n', '')
    # qa_dict = parse_game(html)
    # print "%s questions and answers found." % len(qa_dict)


