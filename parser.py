import re
from string import split
from bs4 import BeautifulSoup
import pymongo


def get_sample_html():
    sample = "samples/game_4529.html"
    with open(sample, "r") as myfile:
        html = myfile.read().replace('\n', '')
    return html


def parse_round(game_round):
    # clue_dict = {}

    clue_list = []

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
                # clue_dict[question] = answer
                clue_list.append({'category': category,
                                  'question,': question,
                                  'answer': answer})

    return clue_list


def write_clues(clue_list):
    coll = pymongo.MongoClient().quest.clues
    for clue in clue_list:
        coll.insert(clue)


def parse_game(page):
    bs = BeautifulSoup(page)
    clue_list = []
    for game_round in ['jeopardy_round', 'double_jeopardy_round']:
        clue_list.append(parse_round(bs.find('div', {'id': game_round})))
    return clue_list


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


if __name__ == '__main__':
    with open(get_sample_html(), "r") as myfile:
        html = myfile.read().replace('\n', '')
    clue_list = parse_game(html)
    write_clues(clue_list)

