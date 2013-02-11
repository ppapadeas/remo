from django.core.urlresolvers import reverse
from jingo import register

from remo.base.utils import number2month
from remo.reports.models import Report


@register.filter
def get_report_edit_url(obj):
    """Return report edit link."""
    up = obj.user.userprofile
    return reverse('reports_edit_report',
                   kwargs={'display_name': up.display_name,
                           'year': obj.month.year,
                           'month': obj.month.strftime('%B')})


@register.filter
def get_report_view_url(obj):
    """Return report view link."""
    up = obj.user.userprofile
    return reverse('reports_view_report',
                   kwargs={'display_name': up.display_name,
                           'year': obj.month.year,
                           'month': obj.month.strftime('%B')})


@register.filter
def get_comment_delete_url(obj):
    """Return the delete url of a comment."""
    up = obj.user.userprofile
    month_name = number2month(obj.report.month.month)
    return reverse('reports_delete_report_comment',
                   kwargs={'display_name': up.display_name,
                           'year': obj.report.month.year,
                           'month': month_name,
                           'comment_id': obj.id})


@register.filter
def get_mentees(user):
    return [mentee_profile.user for mentee_profile in
            user.mentees.order_by('user__last_name', 'user__first_name')]


@register.function
def get_reps_reports(users):
    """Returns the reports of users."""
    reports = []
    for user in users:
        reports += (Report.objects.filter(user=user).
                    order_by('-created_on').distinct()[:20])
    return reports
