from lib import music
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

def default(request):
    """
        Displays lists of entertainment by medium
    """
    albums = music.parse_music()

    return render_to_response('weekly/default.html', {'albums': albums})

