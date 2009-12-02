import urllib2
import datetime
from beautifulsoup import BeautifulSoup

GAMES_URL = 'http://www.metacritic.com/rss/games/xbox360.xml'

def parse_games():
    """ Parses the lastest 10 xbox 360 games from metacritic and returns a dictionary
        in the form {title, link, date}
    """
    games = urllib2.urlopen(GAMES_URL)
    html = BeautifulSoup(games)
    content = html.findAll('item')
    
    return [__cleaned(game) for game in content[:10]]

def __cleaned(game):
    """
        Cleans the games data and returns a dictionary in the form {title, link, date}
    """
    link = game.link.string
    title = " - ".join(map(lambda x: x.strip(), game.title.string.split('-')))
    date = datetime.datetime.strptime(game.pubdate.string[5:16].strip(), '%d %b %Y')
    
    return {'title': title, 'link': link, 'date': date}

if __name__ == '__main__':
    """
        command line
    """
    games = parse_games()
    print games
