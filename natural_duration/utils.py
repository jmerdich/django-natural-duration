def human_duration_string(value):
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
