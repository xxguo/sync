#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
root_mod = '/home/xxguo/Project/task'
sys.path.append(root_mod)
import time
import logging
from setting import LOGGING
from db.mongodb.executor import MongodbQuerApi
from db.mysql.executor import *
from utils.daemon import Daemon
from db.mysql.query import find_keyword
from datetime import datetime, timedelta


logger = logging.getLogger("synTopicTask")


class SynTopicTaskService(Daemon):

    task_curosr = "mongo_sign"
    mongo_task = "zjld"
    mysql_table = ""

    def run(self):
        while True:
            try:
                logger.info("start...")
                task(self.task_curosr, self.mongo_task, self.mysql_table)
                time.sleep(3600) 
            except e:
                logger.info("PROCESS SLEEPPING<%s>..."%e)

def task(mongo_sign, mongo_task, mysql_table):
 
    topics = find_keyword()
    for topic in topics:
        # print '---',topic.review.encode('utf-8')
        # break
        Task(topic.review, mongo_task).type_task()
    # print '======='

class Task(object):

    def __init__(self, key, mongo_task):
        self.key = key
        self.mongo_task = mongo_task

    def insert_task(self, data):
        crawler_conf = {
            "type" : data.get('type',''),
            "status" : data.get('status', 0),
            "priority" : data.get('priority',3),
            "interval" : data.get('interval', 7200),
            "update_time" : datetime.utcnow(),
            "lastrun": datetime.utcnow(),
            "nextrun": datetime.utcnow() - timedelta(days=2),
            "crtetime": datetime.utcnow(),
            "timeout": 3600,
            "key": self.key,
            "data" : {
                "source_type" : u"关键词",
                "source" : data.get('source', '')}
        }

        if not MongodbQuerApi(self.mongo_task).find_one({'type':data.get('type',''),
                    'key': self.key}):
            MongodbQuerApi(self.mongo_task).save(crawler_conf)
            logger.info("INSERT TASK SUCESS CRAWLER: <%s>..."%crawler_conf)
            # print '  ==',self.key.encode('utf-8')
            logger.info("insert_task <%s>..."%self.key)


    def type_task(self):
        types = {
            "baidu": "zjld.baidu.newstitle",
            "weibo": "zjld.weibo.newstitle",
            "sogou": "zjld.sogou.keywords",
        }
        weibodata = {
            "interval": 21600,
            "type": types.get('weibo'),
            "source": 'weibo'
        }

        weibo = self.insert_task(weibodata)

        baidudata = {
            "type": types.get('baidu'),
            "source": 'baidu',
        }
        baidu = self.insert_task(baidudata)

        weixindata = {
            "type": types.get('sogou'),
            "source": 'sogou'
        }
        weixin = self.insert_task(weixindata)
       
if __name__ == '__main__':
    # task('mongo_sign', 'zjld', 'mysql_table')
    daemon = SynTopicTaskService('/tmp/fetch-hot.pid')
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
   
