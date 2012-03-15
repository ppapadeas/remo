from remo.remozilla.models import Status


def get_last_updated_date():
    """Get last successful Bugzilla sync datetime."""
    status = Status.objects.get(pk=1)
    return status.last_updated


def set_last_updated_date(date):
    """Set last successful Bugzilla sync datetime."""
    status = Status.objects.get(pk=1)
    status.last_updated = date
    status.save()
    return status.last_updated
