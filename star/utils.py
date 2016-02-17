# -*- coding: utf-8 -*-

"""
star.utils
~~~~~~~~~~

Utilities.
"""

import datetime

import dateparser


def date(date):
    """Convert string dates (for the lazy)."""
    return datetparser.parse(date, settings={'TIMEZONE': 'US/Eastern'})


def date_range(start, end):
    """Returns a list of dates."""
    start = date(start)
    end = date(end)

    r = (end + datetime.timedelta(days=1) - start).days
    return [start + datetime.timedelta(days=i) for i in range(r)]
