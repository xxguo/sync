# -*- coding: utf-8 -*-
import sys
root_mod = '/home/xxguo/Project/task'
sys.path.append(root_mod)
from db.mongodb.connection import mongo_db

_db = mongo_db()

class MongodbQuerApi(object):

    def __init__(self, table):
        self.table =table


    def save(self, dct):

        def insert():
            _db[self.table].insert(dct)

        insert()

    def find_one(self, dct):

        def result():
            return _db[self.table].find_one(dct)

        return result()

    def update(self, term, dct):

        def result():
            _db[self.table].update(term,dct)

        result()

if __name__ == '__main__':
    pass
