from django.conf.urls.defaults import *
from weekly import views

urlpatterns = patterns('',
    url(r'^$', views.default, name='weekly_default'),    
    url(r'^music/$', views.latest_music, name='weekly_music'),    
    url(r'^games/(?P<category>\w+)/$', views.latest_games, name='weekly_games'),    
)
