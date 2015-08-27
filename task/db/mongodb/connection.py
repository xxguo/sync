from pymongo import MongoClient

_db = None
class MongoClient(object):

    MONGO_CONN_STR = "mongodb://192.168.1.202:27017"
    _conn = MongoClient(MONGO_CONN_STR)
    db = _conn["crawler"]

def mongo_db():
    return _db if _db else MongoClient().db

if __name__ == '__main__':
    mongo_db()