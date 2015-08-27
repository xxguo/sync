# -*- coding: utf-8 -*-
import MySQLdb
from peewee import MySQLDatabase
from playhouse.pool import PooledMySQLDatabase


_MySQLDatabase = None
_MySQLDatabasePool = None

class MySQLClient(object):
    """docstring for MySQL"""
    def __init__(self, conf={}):
        # conf  = {
        #     'host': '115.29.198.218',
        #     'port': '3306',
        #     'user': 'shendu',
        #     'passwd': 'P@55word',
        #     'db': 'yqj2'
        # }
        # conf  = {
        #     'host': '192.168.1.101',
        #     'port': '3306',
        #     'user': 'test',
        #     'passwd': 'password',
        #     'db': 'yqj2'
        # }
        conf  = {
            'host': '192.168.1.161',
            'port': '3306',
            'user': 'shendu',
            'passwd': 'P@55word',
            'db': 'yqj'
        }
        self.conf = conf

    def connect(self):
        db = MySQLdb.connect(host=self.conf["host"], user=self.conf["user"],
            passwd=self.conf["passwd"], db=self.conf["db"])
        return db.cursor()

    def db(self):
        global _MySQLDatabase
        _MySQLDatabase = MySQLDatabase(self.conf["db"], host=self.conf["host"],
            user=self.conf["user"], passwd=self.conf["passwd"])
        return _MySQLDatabase

    def db_pool(self):
        global _MySQLDatabasePool
        _MySQLDatabasePool = PooledMySQLDatabase(self.conf["db"],  host=self.conf["host"],
            user=self.conf["user"], passwd=self.conf["passwd"], max_connections=10,stale_timeout=300)
        return _MySQLDatabasePool



def get_cursor():
    return MySQLClient().connect()


def mysql_db():
    return _MySQLDatabase if _MySQLDatabase else MySQLClient().db()


def mysql_db_pool():
    return _MySQLDatabasePool if _MySQLDatabasePool else MySQLClient().db_pool()



if __name__ == '__main__':
    mysql_db()
