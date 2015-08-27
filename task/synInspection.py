#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
root_mod = '/home/xxguo/Project/task'
sys.path.append(root_mod)
import time
import logging
import MySQLdb, MySQLdb.cursors
from setting import LOGGING
from utils.daemon import Daemon
from db.mysql.query import get_inspectionMaxID ,save_inspection

logger = logging.getLogger("synInspection")

class SynTopicTaskService(Daemon):

    def run(self):
        while True:
            try:
                logger.info("start...")
                lpush()
                time.sleep(3600) 
            except e:
                logger.info("PROCESS SLEEPPING<%s>..."%e)

def lpush():
    yuqing = MySQLdb.connect("218.244.132.40","shendu","P@55word","zjld" ,cursorclass = MySQLdb.cursors.DictCursor)
    maxid =  get_inspectionMaxID() 
    maxid = maxid if maxid else 0
    logger.info("start maxid <%s>"%maxid)
    # print maxid
    cursor_yuqing = yuqing.cursor()
    sql = "select * from inspection where id > '%s'" %(maxid)
    cursor_yuqing.execute(sql)
    results = cursor_yuqing.fetchall()
    for item in results:
        save_inspection(item)
        logger.info("insert <%s>"%item)
        print item['id']
    yuqing.close()



if __name__ == '__main__':
    # lpush()

    daemon = SynTopicTaskService('/tmp/fetch-inspection.pid')
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
