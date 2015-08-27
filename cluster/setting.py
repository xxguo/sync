'''
Settings for crawler

@author: Liuxi Wu
@email : lxwu@shendu.info
'''

import os
import re
from logging import config
from ConfigParser import SafeConfigParser

SRC_PATH = os.path.dirname(__file__)
LOGGERS_NAME = ["syncservice", "fetchservice", "sentimentservice", "synInspection"]

LOG_BASE = None


def _load_config():
    global LOG_BASE

    SECTION = 'syncservice'

    cp = SafeConfigParser()
    cp.read(os.path.join(SRC_PATH, "conf/conf.cfg"))

    LOG_BASE = cp.get(SECTION, 'logs_dir')


def get_logging(loggers_name):
    logging = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s\t%(asctime)s\t%(message)s'
            },
            'detail': {
                'format': '%(levelname)s\t%(asctime)s\t[%(module)s.%(funcName)s line:%(lineno)d]\t%(message)s',
            },
        }
    }
    handlers = {}
    loggers = {}

    for logger_name in loggers_name:
        handlers[logger_name + "_file"] = {
            'level': 'DEBUG',
            'formatter': 'detail',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOG_BASE, logger_name + ".log"),
        }
        handlers[logger_name + "_err_file"] = {
            'level': 'WARN',
            'formatter': 'detail',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOG_BASE, logger_name + "_error.log"),
        }
        loggers[logger_name] = {
            'handlers': [logger_name + '_file',  logger_name + '_err_file'],
            'level': 'DEBUG',
            'propagate': True,
        }

    logging['handlers'] = handlers
    logging['loggers'] = loggers

    return logging

_load_config()

LOGGING = get_logging(LOGGERS_NAME)
config.dictConfig(LOGGING)
