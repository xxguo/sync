
# -*- coding: utf-8 -*-
import traceback
import sys

def get_exception_info():
    exc_type, value, tb = sys.exc_info()
    formatted_tb = traceback.format_tb(tb)
    data = 'Exception %s: %s Traceback=\n%s' % (exc_type, value, ''.join(
        formatted_tb))
    return data
