import os
import requests
import glob
import re
import logging
from bs4 import BeautifulSoup
from random import randint

log = logging.getLogger(__name__)


URL_BASE = 'http://www.j-archive.com/showgame.php?game_id='
SAMPLE_DIR = 'samples'
TEST_GAME_ID = 4529
TEST_SHOW_NUM = 153


def get_random_objs(obj_type, num_returned=1):
    db_count = obj_type.objects.count()
    for i in range(num_returned):
        yield obj_type.objects.all()[randint(0, db_count - 1)]


def get_sample_ids():
    """Gets the ids from the file names in the samples dir.
    """
    files = glob.glob(os.path.join(SAMPLE_DIR, '*.html'))
    for fname in files:
        match = re.search(r'\d+', fname)
        if not match:
            continue
        else:
            yield match.group()


def get_fname(game_id):
    """Returns valid sampledir filename for given id.
    """
    if isinstance(game_id, int):
        game_id = str(game_id)
    return os.path.join(SAMPLE_DIR, "game_{}.html".format(game_id))


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


def save_remote_games(*game_ids):
    """Gets remote games and saves them to db.
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


def trim(txt, length=30):
    if txt and len(txt) > length:
        return txt[:length-1] + '...'


def parse_seasons(count=1):
    """
    Get game_ids from given number of seasons.
    Not recently used or tested.
    """
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

