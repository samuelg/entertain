import datetime
import feedparser

GAMES_URL = 'http://www.metacritic.com/rss/games/xbox360.xml'

def parse_games(json=False):
    """ Parses the lastest 10 xbox 360 games from metacritic and returns a dictionary
        in the form {title, link, date}

        Pass json=True to get games in JSON format.
    """
    content = feedparser.parse(GAMES_URL).entries
    
    return [__cleaned(game, json) for game in content[:10]]

def __cleaned(game, json):
    """
        Cleans the games data and returns a dictionary in the form {title, link, date}
    """
    link = game.link
    title = " - ".join(map(lambda x: x.strip(), game.title.split('-')))
    date = datetime.datetime(*game.updated_parsed[:6])

    # convert date to timestamp
    if json:
        date = date.strftime('%a, %d %b %Y %H:%M:%S %Z')
    
    return {'title': title, 'link': link, 'date': date}

if __name__ == '__main__':
    """
        command line
    """
    games = parse_games()
    print games
