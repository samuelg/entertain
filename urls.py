from django.conf.urls.defaults import *
from django.contrib import admin
from weekly.views import default
import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^weekly/', include('weekly.urls')),
    (r'^$', default),
)

# setup to server static files in development mode
if settings.DEBUG:
    if settings.MEDIA_URL.startswith("/"):
        media_url = settings.MEDIA_URL[1:]
        urlpatterns += patterns('',
            (r'^%s(?P<path>.*)$' % media_url, 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        )

