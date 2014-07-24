import requests
from bs4 import BeautifulSoup

URL_BASE = 'http://www.j-archive.com/showgame.php?game_id='


def trim(txt):
    if txt and len(txt) > 10:
        return txt[:9] + '...'


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


def save_game(game_id):
    url = URL_BASE + game_id
    html = requests.get(url).text
    outfile = open('samples/game_{}.html'.format(game_id), 'w')
    outfile.write(html)
    outfile.close()


def save_games():
    with open('samples/season_ids.txt', "r") as myfile:
        for season_id in myfile:
            save_game(season_id.replace('\n', ''))


# if __name__ == '__main__':
#     pass
#     # save_games()



# def get_page(game_id):
#     url = URL_BASE + game_id
#     return requests.get(url).text



# outfile = open('season_ids.txt', 'w')
# for sid in sids:
#     outfile.write(sid + '\n')
# outfile.close()


