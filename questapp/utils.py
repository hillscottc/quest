import requests
from bs4 import BeautifulSoup
import re


def trim(txt):
    if txt and len(txt) > 10:
        return txt[:9] + '...'


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
