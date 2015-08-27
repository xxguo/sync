# -*- coding: utf-8 -*-

import sys
root_mod = '/home/lxwu/Documents/shendu/sync/cluster'
#root_mod = '/home/chzhao/CRM/sync/cluster'
sys.path.append(root_mod)

from snownlp import SnowNLP
from db.mysql import query


def extract_title(title):
    s = SnowNLP(title)
    return s.words


def get_area(words=[]):
    return map(query.get_area_by_name, words)


if __name__ == '__main__':
    a = u'\u5168\u56fd'.encode("utf-8")
    print a
    # words = extract_title(u"昆明黑心商贩在米线中添加国家禁用防腐剂")
    # areas = get_area(words)

    # for a in areas:
    #     if a.count() >= 1:
    #         print a[0].id, a[0].name.encode("utf-8")
