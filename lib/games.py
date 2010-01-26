import datetime
import feedparser

BASE_GAMES_URL = 'http://www.metacritic.com/rss/games/'
SYSTEMS = { 'xbox': 'xbox360.xml',
            'wii': 'wii.xml',
            'ds': 'ds.xml',
            'ps3': 'ps3.xml',
            'pc': 'pc.xml'
          }

def parse_games(game_system='xbox', json=False):
    """ Parses the lastest 10 xbox 360, wii, and DS games from metacritic and returns a dictionary
        in the form {title, link, date}

        Pass json=True to get games in JSON format.
    """

    content = feedparser.parse('%s%s' % (BASE_GAMES_URL, SYSTEMS[game_system])).entries[:10]
    return [__cleaned(game, json) for game in content]

def __cleaned(game, json):
    """
        Cleans the games data and returns a dictionary in the form {title, link, date}
    """
    link = game.link
    title = " - ".join(map(lambda x: x.strip(), game.title.split('-')))
    date = datetime.datetime(*game.updated_parsed[:6])

    # convert date to timestamp
    if json:
        date = date.strftime('%a, %d %b %Y')
    
    return {'title': title, 'link': link, 'date': date}

if __name__ == '__main__':
    """
        command line
    """
    games = parse_games()
    print games
