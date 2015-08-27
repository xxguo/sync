# -*- coding: utf-8 -*-

import sys
root_mod = '/home/xxguo/Project/sync/cluster'
sys.path.append(root_mod)

import logging
import time
from setting import LOGGING
from datetime import datetime, timedelta
from utils.daemon import Daemon
from db.redis.executor import RedisQueryApi
from db.mysql.query import *


logger = logging.getLogger("fetchservice")


class FetchTopicService(Daemon):

    redis_name = "weibohot"
    column_family = "hot"
    sort_redis = "sort_weibohot"

    def run(self):
        while True:
            try:
                logger.info("start...")
                lpush(self.redis_name, self.column_family, self.sort_redis)
            except e:
                logger.info("PROCESS SLEEPPING<%s>..."%e)


def lpush(redis_name, column_family, sort_redis):
    if RedisQueryApi().scard(redis_name):
        RedisQueryApi().sort(name=redis_name,
            by="weibohot*->reposts", desc=False, store=column_family)
        RedisQueryApi().delete(sort_redis)
        for item in RedisQueryApi().lrange(column_family, 0, -1):
            
            logger.info("PROCESS SLEEPPING<%s>..."%item)
            item = redis_name + item
            data = RedisQueryApi().hgetall(item)
            uuid = data['id']
            try:
                weibos = get_weibo(uuid)
            except:
                continue
            data['publisher'] = weibos.publisher.publisher
            data['photo'] = weibos.publisher.photo
            data['brief'] = weibos.publisher.brief
            data['id'] = weibos.id
            data['title'] = weibos.title
            data['url'] = weibos.url
            data['author'] = weibos.author
            data['pubtime'] = weibos.pubtime
            data['content'] = weibos.content

            new_data = model(data)
            pubtime = data['pubtime']
            exce_time = datetime.now() - timedelta(days=35)
            if pubtime > exce_time:
                RedisQueryApi().lpush(sort_redis ,str(new_data))
            else:
                RedisQueryApi().srem(redis_name,uuid)
                RedisQueryApi().delete(item)

        time.sleep(3600)
    else:
        logger.info("PROCESS SLEEPPING<time.sleep(60)>...")
        time.sleep(60)
                

def model(data={}):
    new_data = {
        "id": str(data["id"]),
        "publisher": data["publisher"],
        "photo": data["photo"],
        "brief": data["brief"],
        "title": data["title"],
        "content": data["content"],
        "url": data["url"],
        "author": data["author"],
        "pubtime": int(time.mktime(data['pubtime'].timetuple())),
        "reposts_count": data["reposts"],
        "comments_count": data["comments"],
        "attitudes_count": data["likes"]
    }

    return new_data
        

if __name__ == '__main__':
    # redis_name = "weibohot"
    # column_family = "hot"
    # sort_redis = "sort_weibohot"
    # lpush(redis_name, column_family, sort_redis)
    daemon = FetchTopicService('/tmp/fetch-hot.pid')
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
        