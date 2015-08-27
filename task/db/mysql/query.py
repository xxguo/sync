# -*- coding: utf-8 -*-

import sys
root_mod = '/home/lxwu/Documents/shendu/cluster'
sys.path.append(root_mod)

from datetime import timedelta
from utils.transform import fromtimestamp
from db.cassandra.executor import CassandraQueryApi
from db.mysql.models import Topic, Inspection, Keyword
from peewee import *


def get_topic(id):
    """
    Get Single Topic Instance
    """
    return Topic.select().where(Topic.id > id)

def get_inspectionMaxID():
    """
    Get Single inspection max id Instance
    """
    return Inspection.select(fn.Max(Inspection.id)).scalar()
def find_keyword():
    """
    Get Single Keyword Instance
    """
    return Keyword.select().where(Keyword.review != '')

def save_inspection(data):
    inspection = Inspection(
        id=data['id'],
        url=data['url'],
        name=data['name'],
        manufacturer=data['manufacturer'],
        qualitied=data['qualitied'],
        pubtime=data['pubtime'],
        product=data['product'],
        source=data['source'],
        province=data['province'],
        city=data['city'],
        district=data['district'],
        create_at=data['create_at'],
        update_at = data['update_at']

    )
    inspection.save(force_insert=True)
    # try:
    #     inspection.save(force_insert=True)
    # except:
    #     inspection.save()
    return inspection
