# -*- coding: utf-8 -*-

import sys
root_mod = '/home/lxwu/Documents/shendu/sync/cluster'
sys.path.append(root_mod)

import logging
import time
from setting import LOGGING
from datetime import datetime
from utils.daemon import Daemon
from db.redis.executor import RedisQueryApi
from db.cassandra.executor import CassandraQueryApi


logger = logging.getLogger("fetchservice")


class FetchWeixinService(Daemon):

    redis_name = "weixin"
    column_family = "weixin"

    def run(self):
        while True:
            lpush(self.redis_name, self.column_family)


def lpush(redis_name, column_family):
    if RedisQueryApi().llen(redis_name) < 100:
        lindex_0 = RedisQueryApi().lindex(redis_name, 0)
        crtime_int = eval(lindex_0)["crtime_int"] if lindex_0 else 0
        rows = fetch(column_family, crtime_int)
        if not rows:
            time.sleep(100)
            logger.info("PROCESS SLEEPPING<NO MORE ROWS>...")

        for row in rows:
            RedisQueryApi().lpush(redis_name, model(row))
    else:
        time.sleep(10)
        logger.info("PROCESS SLEEPPING<QUEUE FULL>...")


def fetch(column_family, crtime_int):
    cql = "SELECT * FROM %s WHERE crtime_int > %s LIMIT 10 ALLOW FILTERING" % \
        (column_family, crtime_int)
    logger.info(cql)

    return CassandraQueryApi().find(cql)

def model(data={}):
    new_data = {
        "id": str(data["id"]),
        "province": data["province"],
        "city": data["city"],
        "district": data["district"],
        "url": data["url"],
        "title": data["title"],
        "content": data["content"],
        "author": data["author"],
        "source": data["source"],
        "type": data["type"],
        "publisher": data["publisher"],
        "pubtime": int(time.mktime(data['pubtime'].timetuple())),
        "crtime_int": data["crtime_int"],
        "origin_source": data["origin_source"],
        "key": data.get("key")
    }

    return new_data
        

if __name__ == '__main__':
    daemon = FetchWeixinService('/tmp/fetch-weixin.pid')
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
        