# -*- coding: utf-8 -*-
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory


_SESSION = None

class CassandraClient(object):
    session = None
    conn = None

    def __init__(self):
        self.conn = {
            'hosts': '192.168.1.201,192.168.1.202,192.168.1.203',
            # 'hosts': '192.168.1.118',
            'port': '9042',
            'username': '',
            'password': ''
        }

    def connect(self, keyspace):
        cluster = Cluster(contact_points=self.conn['hosts'].split(','),
            port=self.conn['port'], auth_provider=PlainTextAuthProvider(
            username=self.conn['username'], password=self.conn['password']))
        metadata = cluster.metadata
        self.session = cluster.connect(keyspace)

    def close(self):
        self.session.cluster.shutdown()


def get_session():
    global _SESSION
    if not _SESSION:
        client = CassandraClient()
        client.connect('zjld')
        client.session.row_factory = dict_factory
        _SESSION = client.session
    return _SESSION


def close_session():
    CassandraClient().close()


if __name__ == '__main__':
    print get_session()
