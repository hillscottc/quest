import os
import logging
import re
import json
from bs4 import BeautifulSoup
import requests
from django.conf import settings
from questapp.parser import parse_game_html
from django.core import serializers
from questapp.models import Clue

log = logging.getLogger(__name__)

URL_BASE = 'http://www.j-archive.com/showgame.php?game_id='
TEST_GAME_ID = 4529
TEST_SHOW_NUM = 153


def write_json(clues):
    jdata = [clue.get_json() for clue in clues]
    # print json.dumps(jdata, indent=2)
    with open("clues.json", "w") as out:
        json.dump(jdata, out, indent=4)


def get_fname(game_id):
    """Returns valid sampledir filename for given id.
    """
    if isinstance(game_id, int):
        game_id = str(game_id)
    return os.path.join(settings.JEAP_SRC_DIR, "game_{}.html".format(game_id))


def write_game(game_id, html):
    """Save html as a file in the SAMPLE_DIR, named with the id.
    """
    if len(html) < 3000:
        return

    fname = get_fname(game_id)
    try:
        with open(fname, "w") as outfile:
            outfile.write(html.encode('utf-8'))
        return fname
    except UnicodeEncodeError as uni_err:
        log.warn("Unicode error writing game {}, {}".format(fname, uni_err))
        return None


def get_remote_html(game_id):
    """Makes http request to host, returns html text.
    """
    game_id = str(game_id) if isinstance(game_id, int) else game_id
    url = URL_BASE + game_id
    return requests.get(url).text


def get_game_ids(season_id_start=30, season_id_end=31):
    """Yields game_ids by parsing source season pages.
    """
    url = 'http://www.j-archive.com/showseason.php?season='
    ids = range(season_id_start, season_id_end)
    for seas_id in ids:
        season_url = url + str(seas_id + 1)
        print 'Getting', season_url
        soup = BeautifulSoup(requests.get(season_url).text)
        for tag in soup.find_all('a'):
            if 'game_id' in tag['href']:
                match = re.search('\d+', tag['href'])
                if match:
                    yield match.group(0)


def save_remote_games(*game_ids):
    """Gets remote games and saves them to db. See SRC_GAME_IDS for an existing big list.
    Or pass in a new list from get_game_ids().
    """
    for game_id in game_ids:
        html = get_remote_html(game_id)
        write_game(game_id, html)


def read_local_html(game_id):
    """Reads and returns local game file text.
    """
    game_id = str(game_id) if isinstance(game_id, int) else game_id
    fname = get_fname(game_id)
    if not os.path.isfile(fname):
        return
    with open(fname, "r") as myfile:
        html = myfile.read().replace('\n', '')
    return html


def load_samples(num=None):
    created = 0
    clue_count = 0
    err_count = 0

    # Get the ids out of space-delimmed jeap_src_ids.txt file.
    with open(settings.JEAP_ID_FILE) as myfile:
        src_game_ids = myfile.read().split()
    if num:
        src_game_ids = src_game_ids[:int(float(num))]

    for i, game_id in enumerate(src_game_ids):
        html = read_local_html(game_id)
        if not html:
            log.info("%s: Skipping %s, no html." % (i, game_id))
            continue

        game, clues, errors = parse_game_html(html, game_id)
        created += 1
        clue_count += len(clues)
        err_count += len(errors)

        log.info("{}: {}, {} clues, {} parse_errs.".format(i, game, len(clues), len(errors)))

    log.info("Loaded {} Games, {} clues, {} parse_errs.".format(created, clue_count, err_count))
    return created





