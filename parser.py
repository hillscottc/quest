import requests
import re
from string import split
from bs4 import BeautifulSoup


def parse_round(game_round):
    clue_dict = {}

    jrt = game_round.table

    cat_tags = jrt.find_all('tr')[0].find_all('td', {'class': "category_name"})
    cats = [t.text for t in cat_tags]
    print cats

    for row in jrt.find_all('tr')[1:]:
        clues = row.find_all('td', {'class': "clue"})
        if not clues:
            continue

        for i, clue in enumerate(clues):
            if clue.div:
                category = cats[i]
                question, answer = parse_qa_from_div(clue.div)
                print "{}...Q:{} A:{}".format(category, question, answer)
                clue_dict[question] = answer

    return clue_dict


def parse_game(page):
    bs = BeautifulSoup(page)
    for game_round in ['jeopardy_round', 'double_jeopardy_round']:
        clue_dict = parse_round(bs.find('div', {'id': game_round}))
        print "Found", game_round, len(clue_dict), 'clues.'


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
    sample = "samples/game_4529.html"
    with open(sample, "r") as myfile:
        html = myfile.read().replace('\n', '')
    parse_game(html)


