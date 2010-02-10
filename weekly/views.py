from lib import music
from lib import games
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson
from settings import SYSTEMS
from redis import Redis, ConnectionError, ResponseError
import datetime

MUSIC_KEY = 'music:latest'
GAMES_KEY = 'games:latest'

def default(request):
    """
        Displays lists of entertainment by medium
    """
    return render_to_response('weekly/default.html', {'systems': SYSTEMS})

def latest_music(request):
    """
        Returns JSON serialization of the latest music
    """
    r = Redis(db=9)
    results = None
    try:
        # try to get the latest 10 music entries
        results = r.lrange(MUSIC_KEY, 0, 9)
        if results:
            # build results
            albums = build_results(results)

            # check if fetched recently
            fetched = datetime.datetime.strptime(albums[0]['fetched'], '%a, %d %b %Y')
            if fetched + datetime.timedelta(days=1) > datetime.datetime.today():
                results = None
    except ResponseError, e:
        pass

    if not results:
        albums = music.parse_music(json=True)
        # store results in a list
        try:
            for album in albums:
                r.push(MUSIC_KEY, '%s|%s|%s|%s'%(album['title'], album['link'], album['date'], datetime.datetime.today().strftime('%a, %d %b %Y')))
            r.ltrim(MUSIC_KEY, -10, -1)
            r.save()
        except ResponseError, e:
            pass

    return HttpResponse(simplejson.dumps(albums))

def latest_games(request, category='xbox'):
    """
        Returns JSON serialization of the latest games 
    """
    game_results = games.parse_games(category, json=True)
    return HttpResponse(simplejson.dumps(game_results))

def build_results(items):
    """
        Returns the results extracted from redis in the form
        [{'title', 'link', 'date', 'fetched'}]
    """
    results = []
    for item in items:
        attrs = item.split('|')
        results.append({'title': attrs[0], 'link': attrs[1], 'date': attrs[2], 'fetched': attrs[3]})

    return results
    
