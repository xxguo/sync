# -*- coding: utf-8 -*-


import sys
root_mod = '/home/xxguo/Project/sync/cluster'
sys.path.append(root_mod)
# import sys
# root_mod = '/home/lxwu/Documents/shendu/sync/cluster'
#root_mod = '/home/chzhao/CRM/sync/cluster'
sys.path.append(root_mod)

import logging
import time
import jieba
import jieba.posseg as pseg
from snownlp import SnowNLP
from collections import defaultdict
from setting import LOGGING
from core.calculator import cal_values
from utils.transform import convert
from utils.fillter import filter_data
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


def extract_title(title):
    s = SnowNLP(title)
    return s.words


def get_area_by_words(words=[]):
    return map(get_area_by_name, words)


def sync_topic(name="topic"):
    try:
        if queue_len(name) > 1:
            data = deal_rpop(name)
            words = extract_title(data["title"].decode("utf-8"))
            query_areas = get_area_by_words(words)
            areas = []
            for a in query_areas:
                if a.count() > 0:
                    areas.append(a)

            if len(areas) == 0:
                areas = [get_area()]

            for a in areas:
                data["area"] = a[0]
                if data["source"] == u"baidu":
                    data["searchmode"] = 1
                    data["publisher"] = get_article_publisher(data["publisher"]) \
                        if article_publisher_count(data["publisher"]) else save_article_publisher(data)

                    if data["source_type"] == "事件":
                        data["type"] = "topic"
                        article = save_article(data)
                        topic_article = save_topic_article(data, article)

                    elif data["source_type"] == "关键词":
                        data["type"] = "custom"
                        article = save_article(data)
                        if custom_count(data["key"]):
                            custom = get_custom(data["key"])
                        else :
                            custom = save_custom(data)
                            keyword = update_keyword(custom, data)
                        custom_article = save_custom_article(data, article, custom)
                    
                    article_category_articles = save_article_category_articles(
                        data, article, u"其他")

                    relateddata = save_relateddata(data)

                    result = cal_values("article", article.title, article.pubtime)

                    for r in result:
                        save_relateddata_articles(relateddata, r) # Save relateddata for article
                        r_id = get_relateddata(r.uuid) \
                            if relateddata_count(r.uuid) else save_relateddata({'id':r.uuid})
                        save_relateddata_articles(r_id, article) # Save relateddata for r

                    logger.info("SYNC SUCCEED TOPICARTICLE<%s>" % article.uuid)

                elif data["source"] == u"sogou":
                    data["publisher"] = get_weixin_publisher(data["publisher"]) \
                        if weixin_publisher_count(data["publisher"]) else save_weixin_publisher(data)

                    if data["source_type"] == "事件":
                        data["type"] = "topic"
                        weixin = save_weixin(data)                    
                        topic_weixin = save_topic_weixin(data, weixin)

                    elif data["source_type"] == "关键词":
                        data["type"] = "custom"
                        weixin = save_weixin(data)
                        if custom_count(data["key"]):
                            custom = get_custom(data["key"])
                        else :
                            custom = save_custom(data)
                            keyword = update_keyword(custom, data)                          
                        custom_weixin = save_custom_weixin(data, weixin)

                    relateddata = save_relateddata(data)

                    result = cal_values("weixin", weixin.title, weixin.pubtime)

                    for r in result:
                        save_relateddata_weixin(relateddata, r) # Save relateddata for article
                        r_id = get_relateddata(r.uuid) \
                            if relateddata_count(r.uuid) else save_relateddata({'id':r.uuid})
                        save_relateddata_weixin(r_id, weixin) # Save relateddata for r

                    logger.info("SYNC SUCCEED TOPICWEIXIN<%s>" % weixin.uuid)

                elif data["source"] == u"weibo":
                    data["publisher"] = get_weibo_publisher(data["publisher"]) \
                        if weibo_publisher_count(data["publisher"]) else save_weibo_publisher(data)

                    data["attitudes_count"] = 0
                    data["comments_count"] = 0
                    data["reposts_count"] = 0
                    if data["source_type"] == "事件":
                        data["type"] = "topic"
                        weibo = save_weibo(data)
                        topic_weibo = save_topic_weibo(data, weibo)

                    elif data["source_type"] == "关键词":
                        data["type"] = "custom"
                        weibo = save_weibo(data)
                        if custom_count(data["key"]):
                            custom = get_custom(data["key"])
                        else :
                            custom = save_custom(data)
                            keyword = update_keyword(custom, data)
                        custom_weibo = save_custom_weibo(data, weibo)

                    logger.info("SYNC SUCCEED TOPICWEIBO<%s>" % weibo.uuid)

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
            data["area"] = get_area(data["province"], data["city"], data["district"])


            data["type"] = "gov"
            article = save_article(data)

            category = get_category(data['title'], data['content'])

            article_category_articles = save_article_category_articles(
                data, article, category)

            relateddata = save_relateddata(data)

            if not filter_data(data): # do not cal_values
                result = cal_values("article", article.title, article.pubtime)

                for r in result:
                    save_relateddata_articles(relateddata, r) # Save relateddata for article
                    r_id = get_relateddata(r.uuid) \
                            if relateddata_count(r.uuid) else save_relateddata({'id':r.uuid})
                    save_relateddata_articles(r_id, article) # Save relateddata for r

            logger.info("SYNC SUCCEED ARTICLE<%s>" % article.uuid)
        else:
            time.sleep(10)

    except Exception, e:
        # raise e  
        msg = get_exception_info()
        logger.error("SYNC FAILED %s" % msg)


def sync_weixin(name="weixin"):
    try:
        if queue_len(name) > 1:
            data = deal_rpop(name)

            data["publisher"] = get_weixin_publisher(data["publisher"]) \
              if weixin_publisher_count(data["publisher"]) else save_weixin_publisher(data)

            data["type"] = "gov"
            weixin = save_weixin(data) # Weixin Model

            relateddata = save_relateddata(data)

            result = cal_values("weixin", weixin.title, weixin.pubtime)

            for r in result:
                save_relateddata_weixin(relateddata, r) # Save relateddata for article
                r_id = get_relateddata(r.uuid) \
                            if relateddata_count(r.uuid) else save_relateddata({'id':r.uuid})
                save_relateddata_weixin(r_id, weixin) # Save relateddata for r

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

            data["publisher"] = get_weibo_publisher(data["publisher"]) \
              if weibo_publisher_count(data["publisher"]) else save_weibo_publisherublisher(data)

            data["type"] = "gov"
            weibo = save_weibo(data) # Weibo Model

            logger.info("SYNC SUCCEED WEIBO<%s>" % weibo.uuid)
        else:
            time.sleep(10)

    except Exception:   
        msg = get_exception_info()
        logger.error("SYNC FAILED %s" % msg)



if __name__ == '__main__':
    sync_topic()
    # sync_article()
    # sync_weixin()
    # sync_weibo()
