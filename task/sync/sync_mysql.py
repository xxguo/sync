# -*- coding: utf-8 -*-

import sys
root_mod = '/home/lxwu/Documents/shendu/sync/cluster'
#root_mod = '/home/chzhao/CRM/sync/cluster'
sys.path.append(root_mod)

import logging
import time
import jieba
import jieba.posseg as pseg
from collections import defaultdict
from setting import LOGGING
from core.calculator import cal_values
from utils.transform import convert
from utils import get_exception_info
from db.redis.executor import RedisQueryApi
from db.cassandra.executor import CassandraQueryApi
from db.mysql.query import *

logger = logging.getLogger("syncservice")


category_list = {
  u'锅炉':  u'特种设备',
  u'压力容器':    u'特种设备',
  u'气瓶':  u'特种设备',
  u'压力管道':    u'特种设备',
  u'电梯':  u'特种设备',
  u'起重机械':    u'特种设备',
  u'客运索道':    u'特种设备',
  u'游乐设施':    u'特种设备',
  u'标准':  u'标准化',
  u'标准化': u'标准化',
  u'计量':  u'计量',
  u'认证':  u'认证监管',
  u'认定':  u'认证监管',
  u'假冒':  u'稽查打假',
  u'伪劣':  u'稽查打假',
  u'专项':  u'稽查打假',
  u'打假':  u'稽查打假',
  u'稽查':  u'稽查打假',
  u'案件':  u'稽查打假',
  u'战略':  u'质量管理',
  u'制度':  u'质量管理',
  u'名牌':  u'质量管理',
  u'评选':  u'质量管理',
  u'监督':  u'质量监管',
  u'抽查':  u'质量监管',
  u'强制':  u'质量监管',
  u'检验':  u'质量监管',
  u'风险':  u'质量监管',
  u'监控':  u'质量监管',
  u'监督':  u'质量监管',
  u'改革':  u'科技兴检',
  u'规划':  u'科技兴检',
  u'项目':  u'科技兴检',
  u'成果':  u'科技兴检',
  u'创新':  u'科技兴检',
  u'文电':  u'综合',
  u'会务':  u'综合',
  u'机要':  u'综合',
  u'档案':  u'综合',
  u'督办':  u'综合',
  u'信息':  u'综合',
  u'保密':  u'综合',
  u'信访':  u'综合',
  u'宣传':  u'综合',
  u'政务公开':    u'综合',
  u'安全保卫':    u'综合',
  u'后勤':  u'综合',
  u'合格':  u'稽查打假',
  u'不合格': u'稽查打假',
  u'查处':  u'稽查打假',
}


def filter_hot_key(dic):
    res = []
    ls = sorted(list(dic.items()), key=lambda x:x[1], reverse=True)
    ls = ls[:10]
    for x in ls:
        #去除空格（包括\n,全角空格，空格）
        if x[0] in (u'', u' ', u'\n', u'　'):
            continue
        #去除单个字
        if len(x[0]) == 1:
            continue
        #判断该词语的词性
        words = pseg.cut(x[0])
        #保留词性为名词的词语
        for w in words:
            if w.flag == 'n':
                res.append(x[0])
    return res


def extract_hot_key(content):
    seq_list = jieba.cut(content, cut_all=True)
    dic = defaultdict(int)
    for x in seq_list:
        dic[x] += 1
    return filter_hot_key(dic)


def get_category(title, content):
    key_list = jieba.cut(title, cut_all=False)
    for key in key_list:
        try:
            category = category_list[key]
            if category: return category
        except KeyError:
            continue
    for key in extract_hot_key(content):
        try:
            category = category_list[key]
            if category: return category
        except KeyError:
            continue

    return u"其他"


def queue_len(name):
    return RedisQueryApi().llen(name)


def deal_rpop(name):
    return convert(eval(RedisQueryApi().rpop(name)))


def sync_topic(name="topic"):
    try:
        if queue_len(name) > 1:
            data = deal_rpop(name)

            if data["source"] == u"baidu":
                data["searchmode"] = 1
                data["publisher"] = get_article_publisher(data["publisher"]) \
                    if article_publisher_count(data["publisher"]) else save_article_publisher(data)

                article = save_article(data)

                topic_article = save_topic_article(data, article)
                
                article_category_articles = save_article_category_articles(
                    data, article, u"其他")

                relateddata = save_relateddata(data)

                result = cal_values("article", article.title, article.pubtime)

                for r in result:
                    save_relateddata_articles(relateddata, r) # Save relateddata for article
                    save_relateddata_articles(get_relateddata(r.uuid), article) # Save relateddata for r

                logger.info("SYNC SUCCEED TOPICARTICLE<%s>" % article.uuid)

            if data["source"] == u"sogou":
                data["publisher"] = get_weixin_publisher(data["publisher"]) \
                  if weixin_publisher_count(data["publisher"]) else save_weixin_publisher(data)

                weixin = save_weixin(data)

                topic_weixin = save_topic_weixin(data, weixin)

                relateddata = save_relateddata(data)

                result = cal_values("weixin", weixin.title, weixin.pubtime)

                for r in result:
                    save_relateddata_weixin(relateddata, r) # Save relateddata for article
                    save_relateddata_weixin(get_relateddata(r.uuid), weixin) # Save relateddata for r

                logger.info("SYNC SUCCEED TOPICWEIXIN<%s>" % weixin.uuid)
        else:
            time.sleep(10)

    except Exception:   
        msg = get_exception_info()
        logger.error("SYNC FAILED %s" % msg)


def sync_article(name="article"):
    try:
        if queue_len(name) > 1:
            data = deal_rpop(name)

            data["publisher"] = get_article_publisher(data["publisher"]) \
                if article_publisher_count(data["publisher"]) else save_article_publisher(data)

            article = save_article(data)

            category = get_category(data['title'], data['content'])

            article_category_articles = save_article_category_articles(
                data, article, category)

            relateddata = save_relateddata(data)

            result = cal_values("article", article.title, article.pubtime)

            for r in result:
                save_relateddata_articles(relateddata, r) # Save relateddata for article
                save_relateddata_articles(get_relateddata(r.uuid), article) # Save relateddata for r

            logger.info("SYNC SUCCEED ARTICLE<%s>" % article.uuid)
        else:
            time.sleep(10)

    except Exception, e:
        raise e  
        msg = get_exception_info()
        logger.error("SYNC FAILED %s" % msg)


def sync_weixin(name="weixin"):
    try:
        if queue_len(name) > 1:
            data = deal_rpop(name)

            data["publisher"] = get_weixin_publisher(data["publisher"]) \
              if weixin_publisher_count(data["publisher"]) else save_weixin_publisher(data)

            weixin = save_weixin(data) # Weixin Model

            relateddata = save_relateddata(data)

            result = cal_values("weixin", weixin.title, weixin.pubtime)

            for r in result:
                save_relateddata_weixin(relateddata, r) # Save relateddata for article
                save_relateddata_weixin(get_relateddata(r.uuid), weixin) # Save relateddata for r

            logger.info("SYNC SUCCEED WEIXIN<%s>" % weixin.uuid)
        else:
            time.sleep(10)

    except Exception:   
        msg = get_exception_info()
        logger.error("SYNC FAILED %s" % msg)


def sync_weibo(name="weibo"):
    try:
        if queue_len(name) > 1:
            data = deal_rpop(name)

            weibo = save_weibo(data) # Weibo Model

            logger.info("SYNC SUCCEED WEIBO<%s>" % weibo.uuid)
        else:
            time.sleep(10)

    except Exception:   
        msg = get_exception_info()
        logger.error("SYNC FAILED %s" % msg)



if __name__ == '__main__':
    # print category
    # sync_topic()
    sync_article()  
    # sync_weixin()
    # sync_weibo()
