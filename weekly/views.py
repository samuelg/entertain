from lib import music
from lib import games
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

def default(request):
    """
        Displays lists of entertainment by medium
    """
    albums = music.parse_music()
    x360_games = games.parse_games()

    return render_to_response('weekly/default.html', {'albums': albums, 'x360_games': x360_games})

