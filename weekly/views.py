from lib import music
from lib import games
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson
from settings import SYSTEMS

def default(request):
    """
        Displays lists of entertainment by medium
    """
    return render_to_response('weekly/default.html', {'systems': SYSTEMS})

def latest_music(request):
    """
        Returns JSON serialization of the latest music
    """
    albums = music.parse_music(json=True)
    return HttpResponse(simplejson.dumps(albums))

def latest_games(request, category='xbox'):
    """
        Returns JSON serialization of the latest games 
    """
    game_results = games.parse_games(category, json=True)
    return HttpResponse(simplejson.dumps(game_results))

