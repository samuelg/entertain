from django.conf.urls.defaults import *
from django.contrib import admin
from weekly.views import default

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^weekly/', include('weekly.urls')),
    (r'^$', default),
)
