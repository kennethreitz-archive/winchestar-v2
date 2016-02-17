# -*- coding: utf-8 -*-

"""
star.utils
~~~~~~~~~~

Utilities.
"""

import datetime
import dateutil.parser
import pytz


def date(date):
    """Convert string dates (for the lazy)."""
    if isinstance(date, basestring):
        date = dateutil.parser.parse(unicode(date))

    # Provided dates are in EST.
    date = pytz.est.localize(date)

    # Dates only, please.
    assert isinstance(date, datetime.datetime)

    return date


def date_range(start, end):
    """Returns a list of dates."""
    start = date(start)
    end = date(end)

    r = (end + datetime.timedelta(days=1) - start).days
    return [start + datetime.timedelta(days=i) for i in range(r)]
