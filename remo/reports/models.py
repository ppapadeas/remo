import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

import remo.base.utils as baseutils

OVERDUE_DAY = 7


class Report(models.Model):
    """Report Model."""
    user = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    mentor = models.ForeignKey(User, null=True, default=None,
                               related_name="reports_mentored")
    month = models.DateField()
    empty = models.BooleanField(default=False)
    recruits = models.PositiveSmallIntegerField(default=0)
    recruits_comments = models.TextField(blank=True, default='')
    past_items = models.TextField(blank=True, default='')
    next_items = models.TextField(blank=True, default='')
    flags = models.TextField(blank=True, default='')

    class Meta:
        ordering=['-month']
        unique_together = ['user', 'month']

    def get_absolute_url(self):
        up = self.user.userprofile
        return reverse('reports_view_report',
                       kwargs={'display_name': up.display_name,
                               'year': self.month.year,
                               'month': self.month.strftime("%B")})

    @property
    def is_overdue(self):
        return self.created_on.day > OVERDUE_DAY


@receiver(pre_save, sender=Report)
def report_set_mentor_pre_save(sender, instance, **kwargs):
    """Set mentor from UserProfile only on first save."""
    if not instance.id:
        instance.mentor = instance.user.userprofile.mentor


@receiver(pre_save, sender=Report)
def report_set_month_day_pre_save(sender, instance, **kwargs):
    """Set month day to the first day of the month."""
    instance.month = datetime.datetime(year=instance.month.year,
                                       month=instance.month.month, day=1)


@receiver(post_save, sender=Report)
def report_delete_notifications_post_save(sender, instance, **kwargs):
    """Delete notifications related to just filled report."""
    pass


class ReportComment(models.Model):
    """Comments in Report."""
    user = models.ForeignKey(User)
    report = models.ForeignKey(Report)
    created_on = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    class Meta:
        ordering = ['id']

    def get_absolute_delete_url(self):
        up = self.user.userprofile
        month_name = baseutils.number2month(self.report.month.month)
        return reverse('reports_delete_report_comment',
                       kwargs={'display_name': up.display_name,
                               'year': self.report.month.year,
                               'month': month_name,
                               'comment_id': self.id})


class ReportEvent(models.Model):
    """Event in Report Model."""
    report = models.ForeignKey(Report)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, default='')
    link = models.URLField()
    participation_type = models.PositiveSmallIntegerField(
        choices=((1, 'Organizer'),
                 (2, 'Attendee')))


class ReportLink(models.Model):
    """Link in Reports Model."""
    report = models.ForeignKey(Report)
    description = models.CharField(max_length=300)
    link = models.URLField()
