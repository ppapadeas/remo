from datetime import datetime

def get_reports_for_year(user, year):
    """Return a list of reports for year."""
    reports = user.report_set.filter(month__year=year)
    reports_list = []
    for month in range(1,13):
        month_name = datetime(year=2000, day=1, month=month).strftime("%b")
        month_details = {'name': month_name}
        if reports.filter(month__month=month).exists():
            month_details['report'] = reports.get(month__month=month)
        else:
            month_details['report'] = None
        reports_list.append(month_details)

    return reports_list
