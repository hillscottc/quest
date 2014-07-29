import requests
from utils import URL_BASE, get_sample_html, get_game_fname
import pymongo
from parser import parse_game


def write_clues(clue_list):
    coll = pymongo.MongoClient().quest.clues
    for clue in clue_list:
        coll.insert(clue)


def save_games(*game_ids):
    """Pull given games from remote source and save locally."""
    for game_id in game_ids:
        if isinstance(game_id, int):
            game_id = str(game_id)
        url = URL_BASE + game_id
        html = requests.get(url).text
        with open(get_game_fname(game_id), "w") as outfile:
            outfile.write(html)


if __name__ == '__main__':

    # save_games(83, 84)

    with open(get_sample_html(), "r") as myfile:
        html = myfile.read().replace('\n', '')
    clues = list(parse_game(html))
    print clues
    # write_clues(clues)