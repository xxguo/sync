# -*- coding: utf-8 -*-

from db.cassandra.connection import get_session


class CassandraQueryApi(object):
    """Cassandra Query API"""
    session = None

    def __init__(self):
        self.session = get_session()

    def find(self, cql):
        """
        cassandra.query.select syntax
        """

        def result():
            return self.session.execute(cql)

        return result()

    def save(self, cql, fields):
        """
        cassandra.query.insert syntax
        """

        def insert():
            self.session.execute(cql, fields)

        insert()
