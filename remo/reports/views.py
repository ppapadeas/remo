import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render

import forms
import remo.base.utils as utils
from models import Report, ReportComment, ReportEvent, ReportLink


#TODO Caching

def view_report(request, display_name, year, month):
    month_number = utils.month2number(month)
    report = get_object_or_404(Report,
                               user__userprofile__display_name=display_name,
                               month__year=int(year),
                               month__month=month_number)

    if request.method == 'POST':
        report_comment = ReportComment(report=report, user=request.user)
        report_comment_form = forms.ReportCommentForm(request.POST,
                                                      instance=report_comment)
        if report_comment_form.is_valid():
            report_comment_form.save()

            messages.success(request, 'Comment saved.')

            # provide a new clean form
            report_comment_form = forms.ReportCommentForm()
    else:
        report_comment_form = forms.ReportCommentForm()

    report_url = reverse('reports_view_report',
                         kwargs={'display_name': display_name,
                                 'year': year,
                                 'month': month})
    return render(request, "view_report.html",
                  {'report': report,
                   'comments': report.reportcomment_set.all(),
                   'report_comment_form_url': report_url,
                   'report_comment_form': report_comment_form})


def edit_report(request, display_name, year, month):
    user = User.objects.get(userprofile__display_name=display_name)
    year_month = datetime.datetime(year=int(year),
                                   month=utils.month2number(month), day=1)
    report = utils.get_or_create_instance(Report, user=user, month=year_month)

    if request.method == 'POST':
        report_form = forms.ReportForm(request.POST, instance=report)
        report_event_form = forms.ReportEventFormset(request.POST,
                                                     instance=report)
        report_link_form = forms.ReportLinkFormset(request.POST,
                                                   instance=report)

        if (report_form.is_valid() and report_event_form.is_valid() and
            report_link_form.is_valid()):
            report_form.save()
            report_event_form.save()
            report_link_form.save()

            messages.success(request, 'Report successfully created.')

            if request.user == user:
                return redirect('profiles_view_my_profile')
            else:
                redirect_url = reverse('profiles_view_profile',
                                       kwargs={'display_name': display_name})
                return redirect(redirect_url)
    else:
        report_form = forms.Reportform(instance=report)
        report_event_form = forms.ReportEventFormset(instance=report)
        report_link_form = forms.ReportLinkFormset(instance=report)

    return render(request, "edit_report.html",
                  {'report_form':report_form,
                   'report_event_form':report_event_form,
                   'report_link_form':report_link_form,
                   'pageuser': user,
                   'year': year,
                   'month': month})
