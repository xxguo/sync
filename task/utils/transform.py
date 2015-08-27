# -*- coding: utf-8 -*-

import time
import collections
from datetime import datetime, timedelta

def convert(data={}):
    """
    Encode Dict Values to UTF-8
    """

    if isinstance(data, basestring):
        return data.encode('utf-8')
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


def fromtimestamp(timestamp):
    return datetime.fromtimestamp(timestamp)
    