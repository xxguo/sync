# -*- coding: utf-8 -*-

import sys
root_mod = '/home/lxwu/Documents/shendu/sync/cluster'
sys.path.append(root_mod)

import math
import jieba
from db.mysql import query

def compare(a, b):

    a1 = [x for x in a]
    b1 = [x for x in b]

    union = list(set(a1).union(set(b1)))

    a_count = [a1.count(x) for x in union]
    b_count = [b1.count(x) for x in union]

    # Calculator 1

    # numerator = 0
    # denominator1 = 0
    # denominator2 = 0

    # for x in xrange(len(union)):
    #     numerator += a_count[x] * b_count[x]
    #     denominator1 += a_count[x] ** 2
    #     denominator2 += b_count[x] ** 2

    # Calculator 2

    numerator = reduce(lambda x, y: x + y, [(a_count[x] * b_count[x]) for x in xrange(len(union))])
    denominator1 = reduce(lambda x, y: x + y, [(a_count[x] ** 2) for x in xrange(len(union))])
    denominator2 = reduce(lambda x, y: x + y, [(b_count[x] ** 2) for x in xrange(len(union))])

    value = numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))

    return value


if __name__ == '__main__':
    """
    test 1
    """
    # compare(jieba.cut(u"我喜欢看电视，不喜欢看电影"), jieba.cut(u"我不喜欢看电视，也不喜欢看电影"))

    """
    tese from mysql
    """

    title1 = u"中国铝业巨亏162亿元成亏损王"
    articles = query.paginate_article(1, 2000)

    for article in articles:
        if not title1 or not article.title:
            continue
        a = jieba.cut(title1)
        b = jieba.cut(article.title)
        value = compare(a, b)

        if value > 0.2:
            print title1.encode("utf-8"), article.title.encode("utf-8"), value
