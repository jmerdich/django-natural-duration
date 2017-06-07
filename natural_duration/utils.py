from django.utils.translation import ugettext_lazy as _


def human_duration_string(value):
    builder = []
    # a list of tuples like ngettext (but with no subs for single)

    us = abs(value.microseconds)
    seconds = abs(value.seconds)
    days = abs(value.days)
    builder.append((_('a year'),
                    '%d ' + str(_('years')), days // 365))
    builder.append((_('a month'),
                    '%d ' + str(_('months')), days % 365 // 30))
    builder.append((_('a week'),
                    '%d ' + str(_('weeks')), days % 365 % 30 // 7))
    builder.append((_('a day'),
                    '%d ' + str(_('days')), days % 365 % 30 % 7))
    builder.append((_('an hour'),
                    '%d ' + str(_('hours')), seconds // 60 // 60))
    builder.append((_('a minute'),
                    '%d ' + str(_('minutes')), seconds // 60 % 60))
    builder.append((_('a second'),
                    '%d ' + str(_('seconds')), seconds % 60))
    builder.append((_('a millisecond'),
                    '%d ' + str(_('milliseconds')), us // 1000))
    builder.append((_('a microsecond'),
                    '%d ' + str(_('microseconds')), us % 1000))

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
