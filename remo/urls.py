from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


handler404 = 'remo.base.views.custom_404'
handler500 = 'remo.base.views.custom_500'

urlpatterns = patterns('',
    url(r'^$', 'remo.base.views.main', name='main'),

    # profiles
    url(r'^u/', include('remo.profiles.user_urls')),
    url(r'^people/', include('remo.profiles.people_urls')),

    # featuredrep
    url(r'^featured/', include('remo.featuredrep.urls')),

    # browserid
    url(r'^browserid/', include('django_browserid.urls')),

    # login / logout
    url(r'^login/failed/$', 'remo.base.views.login_failed',
        name='login_failed'),
    url(r'^login/plain/$', 'remo.profiles.views.plainlogin',
        {'template_name': 'plainlogin.html'}, name='plainlogin'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),

    url(r'^view_report/$', direct_to_template, {'template': 'view_report_mockup.html'}),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^404/$', handler404),
        (r'^500/$', handler500),
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
