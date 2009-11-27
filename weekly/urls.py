from django.conf.urls.defaults import *
from weekly import views

urlpatterns = patterns('',
    url(r'^$', views.default, name='weekly_default'),    
)
