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
    albums = _fetch_from_redis(MUSIC_KEY)

    if not albums:
        albums = music.parse_music(json=True)
        _store_in_redis(albums, MUSIC_KEY)

    return HttpResponse(simplejson.dumps(albums))

def latest_games(request, category='xbox'):
    """
        Returns JSON serialization of the latest games 
    """
    game_results = games.parse_games(category, json=True)
    return HttpResponse(simplejson.dumps(game_results))

def _fetch_from_redis(redis_key):
    """
        Fetched the given items from Redis.
    """
    r = Redis(db=9)
    results = None
    try:
        # try to get the latest 10 items
        results = r.lrange(redis_key, 0, 9)
        if results:
            # build results
            items = _build_results(results)

            # check if fetched recently
            fetched = datetime.datetime.strptime(items[0]['fetched'], '%a, %d %b %Y')
            if datetime.datetime.today() > fetched + datetime.timedelta(days=1):
                # force a fetch from the feed is fetched over a day ago
                results = None
            else:
                # else return the items fetched from redis
                results = items
    except ResponseError, e:
        pass

    return results

def _store_in_redis(items, redis_key):
    """
        Store the given items in Redis.
    """
    r = Redis(db=9)
    # store results in a list
    try:
        for item in items:
            r.push(redis_key, '%s|%s|%s|%s'%(item['title'], item['link'], item['date'], datetime.datetime.today().strftime('%a, %d %b %Y')))
        r.ltrim(redis_key, -10, -1)
        r.save()
    except ResponseError, e:
        pass

def _build_results(items):
    """
        Returns the results extracted from redis in the form
        [{'title', 'link', 'date', 'fetched_date'}]
    """
    results = []
    for item in items:
        attrs = item.split('|')
        results.append({'title': attrs[0], 'link': attrs[1], 'date': attrs[2], 'fetched': attrs[3]})

    return results

