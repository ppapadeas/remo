import datetime

from django.contrib.auth.models import User
from nose.tools import eq_
from test_utils import TestCase

from remo.reports.models import Report

class ModelTest(TestCase):
    """Tests related to Reports Models."""
    fixtures = ['demo_users.json']

    def setUp(self):
        """Setup tests."""
        self.user = User.objects.get(username="rep")
        month_year = datetime.datetime(year=2012, month=1, day=10)
        self.report = Report(user=self.user, month=month_year)
        self.report.save()

    def test_mentor_set_for_new_report(self):
        eq_(self.report.mentor, self.user.userprofile.mentor)

        # Change user mentor and re-save the report. Report should
        # point to the first mentor.
        old_mentor = self.user.userprofile.mentor
        self.user.userprofile.mentor = User.objects.get(username="counselor")
        self.user.save()

        self.report.save()
        eq_(self.report.mentor, old_mentor)

    def test_overdue(self):
        eq_(self.report.is_overdue, True)

        # Change report created_on, so report is not overdue
        self.report.created_on = datetime.datetime(year=2012, month=2, day=1)
        self.report.save()
        eq_(self.report.is_overdue, False)

        # Change report created_on, to point to the last week of
        # report's month. Should not be overdue.
        self.report.created_on = datetime.datetime(year=2012, month=1, day=30)
        self.report.save()
        eq_(self.report.is_overdue, False)

    def test_set_month_day(self):
        eq_(self.report.month.day, 1)
