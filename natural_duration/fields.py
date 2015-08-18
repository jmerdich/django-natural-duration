# vim: set fileencoding=UTF-8
import re
from datetime import timedelta

from django.forms import Field
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.dateparse import parse_duration
from django.utils.duration import duration_string

MICRO = timedelta(microseconds=1)
MILLIS = timedelta(milliseconds=1)
SECOND = timedelta(seconds=1)
MINUTE = timedelta(minutes=1)
HOUR = timedelta(hours=1)
DAY = timedelta(days=1)
WEEK = timedelta(days=7)
MONTH = timedelta(days=30)
YEAR = timedelta(days=365)
# a mapping of regexes to timedeltas
UNITS = {
    'moment': timedelta(),
    'microsecond': MICRO,
    'micro': MICRO,
    'mic': MICRO,
    'us': MICRO,
    'u': MICRO,
    u'µs': MICRO,
    u'µ': MICRO,
    'millisecond': MILLIS,
    'mil': MILLIS,
    'ms': MILLIS,
    'second': SECOND,
    'sec': SECOND,
    's': SECOND,
    'minute': MINUTE,
    'min': MINUTE,
    'm(?!s)': MINUTE,
    'hour': HOUR,
    'hr': HOUR,
    'h': HOUR,
    'day': DAY,
    'dy': DAY,
    'd': DAY,
    'week': WEEK,
    'wk': WEEK,
    'w': WEEK,
    'month': MONTH,
    'mon': MONTH,
    'mo': MONTH,
    'mth': MONTH,
    'year': YEAR,
    'yr': YEAR,
    'y': YEAR
}


class NaturalDurationField(Field):
    default_error_messages = {
        'invalid': _('Enter a valid duration.'),
    }

    def __init__(self, human_values=True, *args, **kwargs):
        self.human_values = human_values
        super(NaturalDurationField, self).__init__(*args, **kwargs)

    def to_td(self, match, unit):
        value = 0
        string = match.group(1)
        if 'a' in string:
            value = 1
        else:
            try:
                value = int(string)
            except ValueError:
                value = float(string)
                return timedelta(seconds=value * UNITS[unit].total_seconds())
        return value * UNITS[unit]

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, timedelta):
            return value
        value = value.strip()
        if not value:
            return None  # handle values like " "
        td = parse_duration(value)
        if td is not None:
            return td
            # The default parser got it. Yay.
        # remove niceties
        value = re.sub(r'(\.(?!\d)|&|and|,)', " ", value, flags=re.I)
        td = timedelta()
        for unit in UNITS:
                regex = r"((\d+\.\d+)|\d+|(?=\s|\d|\b)a(n(?=\s|\d|\b))?)\s?(" \
                    + unit \
                    + r"s?(?=\s|\d|\b))"

                matches = re.finditer(regex,
                                      value,
                                      flags=re.I | re.U)
                for match in matches:
                    td = td + self.to_td(match, unit)
                value = re.sub(regex, "", value, flags=re.I | re.U)
        if value.strip():
            # there's stuff left. KILL IT
            raise ValidationError(self.default_error_messages['invalid'])
        return td

    def prepare_value(self, value):
        # humanize had too much rounding...
        # also, always assuming positive for now
        if value is None:
            return None
        if not isinstance(value, timedelta):
            return value
        if not self.human_values:
            return duration_string(value)
        elif value == timedelta():
            return "a moment"
        builder = []
        # a list of tuples like ngettext (but with no subs for single)

        us = abs(value.microseconds)
        seconds = abs(value.seconds)
        days = abs(value.days)
        builder.append(('a year', '%d years', days // 365))
        builder.append(('a month', '%d months', days % 365 // 30))
        builder.append(('a week', '%d weeks', days % 365 % 30 // 7))
        builder.append(('a day', '%d days', days % 365 % 30 % 7))
        builder.append(('an hour', '%d hours', seconds // 60 // 60))
        builder.append(('a minute', '%d minutes', seconds // 60 % 60))
        builder.append(('a second', '%d seconds', seconds % 60))
        builder.append(('a millisecond', '%d milliseconds', us // 1000))
        builder.append(('a microsecond', '%d microseconds', us % 1000))

        legit = []
        for tup in builder:
            if tup[2] == 0:
                continue
            elif tup[2] == 1:
                legit.append(tup[0])
            else:
                legit.append(tup[1] % tup[2])
        if len(legit) == 1:
            return legit[0]
        elif len(legit) == 2:
            return legit[0] + " and " + legit[1]
        return ", ".join(legit[:-1]) + ", and " + legit[-1]
