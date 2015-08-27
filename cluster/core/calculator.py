# -*- coding: utf-8 -*-
import jieba
from core.TF_IDF import compare
from db.mysql.query import get_muti_article, \
    get_muti_weixin, get_muti_weibo


def comparison_data(type, pubtime):
    if type == "article":
        return get_muti_article(pubtime, interval=7)
    elif type == "weixin":
        return get_muti_weixin(pubtime, interval=7)
    elif type == "weibo":
        return get_muti_weibo(pubtime, interval=7)


def cal_values(type, title, pubtime):
    """
    Calculate Similar Data

    Return Type List [<Article>, ?, ?]
    """

    result = []
    for article in comparison_data(type, pubtime):
        if not title or not article.title:
            continue
        value = compare_title(title, article.title)
        
        if value > 0.6:
            result.append(article)

    return result

def compare_title(a, b):
    a = jieba.cut(a)
    b = jieba.cut(b)
    return compare(a, b)
    