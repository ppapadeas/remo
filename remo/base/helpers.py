import base64
import binascii
import re
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.markup.templatetags import markup
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from jingo import register
from jinja2 import Markup

from Crypto.Cipher import AES

AES_PADDING = 16
AES_IV_LENGTH = 16


@register.filter
def markdown(text):
    """Return text rendered as Markdown."""
    return Markup(markup.markdown(text, 'safe'))


@register.filter
def get_display_name(obj):
    """Return obj display_name if obj is User. Otherwise return None."""
    if isinstance(obj, User):
        return obj.userprofile.display_name


@register.filter
def format_datetime(obj, type=None):
    """Return datetime obj formatted."""
    if type == 'full':
        return obj.strftime('%d %B %Y %H:%M')
    return obj.strftime('%Y-%m-%d %H:%M')


@register.filter
def format_datetime_iso(obj):
    """Return datetime obj ISO formatted."""
    return obj.strftime('%Y-%m-%dT%H:%M:%S')


@register.filter
def format_datetime_unix(obj):
    """Return unix representation of obj."""
    return time.mktime(obj.timetuple())


@register.filter
def format_datetime_utc(obj):
    """Return datetime object UTC formatted."""
    return obj.strftime('%Y%m%dT%H%M%S')


@register.filter
def strftime(obj, style):
    """Return string of datetime object formatted with style."""
    return obj.strftime(style)


@register.function
def get_static_map_url(width, height, lon, lat, zoom=4):
    """Return static map url."""
    api_key = settings.CLOUDMADE_API
    marker_id = settings.CLOUDMADE_MARKER_85
    URL = ('http://staticmaps.cloudmade.com/%(api_key)s/staticmap?'
           'styleid=997&size=%(width)sx%(height)s&center=%(lon)s,%(lat)s'
           '&zoom=%(zoom)s&marker=id:%(marker_id)s|%(lon)s,%(lat)s')
    return URL % {'api_key': api_key, 'width': width, 'height': height,
                  'marker_id': marker_id, 'lat': lat, 'lon': lon,
                  'zoom': zoom}


@register.function
def get_next_url(request):
    """Return next_url stored in session or Dashboard."""
    if 'next_url' in request.session:
        return request.session.pop('next_url')
    elif request.get_full_path() == '/':
        return reverse('dashboard')

    return request.get_full_path()


def pad_string(str, block_size):
    """Pad string to reach block_size."""
    numpad = block_size - (len(str) % block_size)
    return str + numpad * chr(numpad)


def enc_string(str):
    """Return AES CBC encrypted string."""
    key = binascii.unhexlify(settings.MAILHIDE_PRIV_KEY)
    mode = AES.MODE_CBC
    iv = '\000' * AES_IV_LENGTH
    obj = AES.new(key, mode, iv)
    return obj.encrypt(str)


@register.filter
def mailhide(value):
    """Return MailHided email address.

    Code from https://code.google.com/p/django-mailhide-filter
    """
    args = {}
    padded_value = pad_string(value, AES_PADDING)
    encrypted_value = enc_string(padded_value)

    args['public_key'] = settings.MAILHIDE_PUB_KEY
    args['encrypted_email'] = base64.urlsafe_b64encode(encrypted_value)
    args['domain'] = value[value.index('@') + 1:]
    args['email'] = value[0]

    result = ("""<a href="http://mailhide.recaptcha.net/d?k=%(public_key)s&"""
              """c=%(encrypted_email)s" onclick="window.open('"""
              """http://mailhide.recaptcha.net/d?k=%(public_key)s&"""
              """c=%(encrypted_email)s', '', 'toolbar=0,scrollbars=0,"""
              """location=0,statusbar=0,menubar=0,resizable=0,width=500,"""
              """height=300'); return false;" title="Reveal this e-mail"""
              """ address">%(email)s...@%(domain)s</a>""") % args

    return Markup(result)


@register.filter
def get_bugzilla_url(bug_id):
    """Return bugzilla url for bug_id."""
    return u'https://bugzilla.mozilla.org/show_bug.cgi?id=%d' % bug_id


@register.function
def active(request, pattern):
    """Return 'active-nav' string when pattern matches request's full path."""
    if re.match(pattern, request.get_full_path()):
        return 'active-nav'

    return None


@register.function
def get_development_environment():
    """Return settings.TEMPLATE_DEBUG."""
    return getattr(settings, 'TEMPLATE_DEBUG', False)


@register.function
def field_with_attrs(bfield, **kwargs):
    """Allows templates to dynamically add html attributes to bound
    fields from django forms.

    Taken from bedrock.
    """
    bfield.field.widget.attrs.update(kwargs)
    return bfield


@register.function
def field_errors(field):
    """Return string with rendered template with field errors."""
    return Markup(render_to_string('form-error.html', {'field': field}))


@register.function
def get_full_name(user):
    """Return user's fullname bugzilla style."""
    return u'%s :%s' % (user.get_full_name(), user.userprofile.display_name)


@register.function
def user_is_mozillian(user):
    """Check is a user belongs to Mozillians's group."""
    return user.groups.filter(name='Mozillians').exists()


@register.function
def user_is_rep(user):
    """Check is a user belongs to Rep's group."""
    return user.groups.filter(name='Rep').exists()
