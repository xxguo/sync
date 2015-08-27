# -*- coding: utf-8 -*-

import sys
root_mod = '/home/lxwu/Documents/shendu/sync/cluster'
sys.path.append(root_mod)

import logging
import sys
import time
from setting import LOGGING
from utils.daemon import Daemon
from snownlp import SnowNLP
from db.mysql import query

logger = logging.getLogger("sentimentservice")


class Sentiment(Daemon):

    def run(self):
        while True:
            sentiment()


def sentiment():
    if query.count() > 0:
        articles = query.paginate_article(1, 100)

        for article in articles:
            if article.title:
                s = SnowNLP(article.title)
                article.feeling_factor = s.sentiments
            else:
                article.feeling_factor = -2

            article.save()
            
            logger.info("Sentiment SUCCEED ARTICLE<%s>" % article.uuid)
    else:
        time.sleep(10)


if __name__ == '__main__':
    daemon = Sentiment('/tmp/sentiment.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)

    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
