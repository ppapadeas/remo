from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'dashboard/$', 'remo.base.views.dashboard', name='dashboard'),
    url(r'dashboard/emailmentees/$', 'remo.base.views.email_mentees',
        name='email_mentees'),
    url(r'about/$', direct_to_template, {'template': 'about.html'},
        name='about'),
    url(r'faq/$', direct_to_template, {'template': 'faq.html'},
        name='faq'),
    url(r'^$', 'remo.base.views.main', name='main'),
    url(r'event_mockup/$', direct_to_template, {'template': 'event_mockup.html'}),
    url(r'event_mockup_edit/$', direct_to_template, {'template': 'event_mockup_edit.html'}),
    url(r'events_mockup/$', direct_to_template, {'template': 'events_mockup.html'}),
)
