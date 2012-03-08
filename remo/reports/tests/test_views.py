from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from nose.tools import eq_
from test_utils import TestCase

from remo.reports.models import ReportComment


class ViewsTest(TestCase):
    """Tests related to Reports Views."""
    fixtures = ['demo_users.json',
                'demo_reports.json']


    def setUp(self):
        """Setup tests."""
        self.user = User.objects.get(username='rep')
        self.up = self.user.userprofile

        self.data = {'empty': False,
                     'recruits': '10',
                     'recruits_comments': 'This is recruit comments.',
                     'past_items': 'This is past items.',
                     'next_items': 'This is next items.',
                     'flags': 'This is flags.',
                     'delete_report': False,
                     'reportevent_set-TOTAL_FORMS':'1',
                     'reportevent_set-INITIAL_FORMS':'0',
                     'reportevent_set-MAX_NUM_FORMS':'',
                     'reportevent_set-0-id': '',
                     'reportevent_set-0-name': 'Event name',
                     'reportevent_set-0-description': 'Event description',
                     'reportevent_set-0-link': 'http://example.com/evtlnk',
                     'reportevent_set-0-participation_type':'1',
                     'reportevent_set-0-DELETE': False,
                     'reportlink_set-TOTAL_FORMS':'1',
                     'reportlink_set-INITIAL_FORMS':'0',
                     'reportlink_set-MAX_NUM_FORMS':'',
                     'reportlink_set-0-id':'',
                     'reportlink_set-0-link':'http://example.com/link',
                     'reportlink_set-0-description':'This is description',
                     'reportlink_set-0-DELETE': False}


    def test_view_report_page(self):
        # check that there is comment
        # check that there is comment form
        c = Client()
        response = c.get(reverse('reports_view_report',
                                 kwargs={'display_name': self.up.display_name,
                                         'year': '2012',
                                         'month': 'January'}))
        self.assertTemplateUsed(response, 'view_report.html')


    def test_view_nonexistent_report_page(self):
        c = Client()
        response = c.get(reverse('reports_view_report',
                                 kwargs={'display_name': self.up.display_name,
                                         'year': '2011',
                                         'month': 'January'}))
        self.assertTemplateUsed(response, '404.html')


    def test_view_edit_report_page(self):
        # test my edit report
        # test without permission other user's
        # test with permission other user's
        # test with report from the future

        edit_page_url = reverse('reports_edit_report',
                                kwargs={'display_name': self.up.display_name,
                                        'year': '2011',
                                        'month': 'February'})

        # Try to access edit report page as anonymous.
        c = Client()
        response = c.get(edit_page_url, follow=True)
        self.assertTemplateUsed(response, 'main.html')
        for m in response.context['messages']:
            pass
        eq_(m.tags, u'warning')

        # Try to access edit report page as owner.
        c.login(username='rep', password='passwd')
        response = c.get(edit_page_url, follow=True)
        self.assertTemplateUsed(response, 'edit_report.html')

        # Try to access edit report page as admin.
        c.login(username='admin', password='passwd')
        response = c.get(edit_page_url, follow=True)
        self.assertTemplateUsed(response, 'edit_report.html')

        # Try to access edit report page as other user.
        c.login(username='mentor', password='passwd')
        response = c.get(edit_page_url, follow=True)
        self.assertTemplateUsed(response, 'main.html')
        for m in response.context['messages']:
            pass
        eq_(m.tags, u'error')


    def test_post_comment_on_report(self):
        # Test with anonymous user.
        c = Client()
        report_view_url = reverse('reports_view_report',
                                  kwargs={'display_name': self.up.display_name,
                                          'year': '2012',
                                          'month': 'January'})
        response = c.post(report_view_url, {'comment': 'This is comment'},
                          follow=True)
        self.assertTemplateUsed(response, 'main.html')
        for m in response.context['messages']:
            pass
        eq_(m.tags, u'error')

        # Test with logged in user.
        c.login(username='mentor', password='passwd')
        response = c.post(report_view_url, {'comment': 'This is comment'},
                          follow=True)
        self.assertTemplateUsed(response, 'view_report.html')
        for m in response.context['messages']:
            pass
        eq_(m.tags, u'success')
        self.assertIn('This is comment', response.content)


    def test_edit_report(self):
        pass

    def test_delete_report(self):
        c = Client()
        delete_url = reverse('reports_edit_report',
                             kwargs={'display_name': self.up.display_name,
                                     'year': '2012',
                                     'month': 'February'})
        tmp_data = self.data.copy()
        tmp_data['delete_report'] = True

        # Test with anonymous user.
        response = c.post(delete_url, tmp_data, follow=True)
        self.assertTemplateUsed(response, 'main.html')
        for m in response.context['messages']:
            pass
        eq_(m.tags, u'warning')

        # Test with logged in user.
        c.login(username='mentor', password='passwd')
        response = c.post(delete_url, tmp_data, follow=True)
        self.assertTemplateUsed(response, 'main.html')
        for m in response.context['messages']:
            pass
        eq_(m.tags, u'error')

        # Test with owner.
        c.login(username='rep', password='passwd')
        response = c.post(delete_url, tmp_data, follow=True)
        self.assertTemplateUsed(response, 'main.html')
        for m in response.context['messages']:
            pass
        eq_(m.tags, u'error')

        print "admin"
        # Test with admin.
        c.login(username='admin', password='passwd')
        response = c.post(delete_url, tmp_data, follow=True)
        self.assertTemplateUsed(response, 'profiles_view.html')
        for m in response.context['messages']:
            pass
        eq_(m.tags, u'success')

    def test_delete_comment(self):
        c = Client()
        delete_url = reverse('reports_delete_report_comment',
                             kwargs={'display_name': self.up.display_name,
                                     'year': '2012',
                                     'month': 'February',
                                     'comment_id': '9'})

        # Test with anonymous user.
        response = c.post(delete_url, {}, follow=True)
        self.assertTemplateUsed(response, 'main.html')
        for m in response.context['messages']:
            pass
        eq_(m.tags, u'warning')

        # Test with other user.
        c.login(username='mentor', password='passwd')
        response = c.post(delete_url, {}, follow=True)
        self.assertTemplateUsed(response, 'main.html')
        for m in response.context['messages']:
            pass
        eq_(m.tags, u'error')

        # Test with admin.
        c.login(username='admin', password='passwd')
        response = c.post(delete_url, {}, follow=True)
        self.assertTemplateUsed(response, 'view_report.html')
        for m in response.context['messages']:
            pass
        eq_(m.tags, u'success')
        eq_(ReportComment.objects.filter(pk=9).exists(), False)


