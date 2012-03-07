from django.conf.urls.defaults import *

urlpatterns = patterns('remo.reports.views',
    url(r'^(?P<year>\d+)/(?P<month>\w+)/$', 'view_report',
        name='reports_view_report'),
    url(r'^(?P<year>\d+)/(?P<month>\w+)/edit/$', 'edit_report',
        name='reports_edit_report')
)
