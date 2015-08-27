#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
root_mod = '/home/lxwu/Documents/shendu/cluster'
sys.path.append(root_mod)

from utils.daemon import Daemon
from sync.sync_mysql import sync_topic, \
    sync_article, sync_weixin, sync_weibo


class SyncTopicService(Daemon):
    def run(self):
        while True:
            sync_topic()


if __name__ == "__main__":
    daemon = SyncTopicService('/tmp/topic-daemon.pid')
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
