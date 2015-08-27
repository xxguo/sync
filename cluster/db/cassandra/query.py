# -*- coding: utf-8 -*-
from db.cassandra.executor import CassandraQueryApi

def get_data(column_family, id):
    """
    Select from Cassandra
    Get singel data
    """

    cql = "SELECT id, title FROM %s WHERE id=%s LIMIT 1" % (column_family, id)
    row = CassandraQueryApi().find(cql)[0]
    return row
