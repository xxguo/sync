# -*- coding: utf-8 -*-

import sys
root_mod = '/home/lxwu/Documents/shendu/cluster'
sys.path.append(root_mod)

from datetime import timedelta
from utils.transform import fromtimestamp
from db.mysql.models import Area, WeixinPublisher, Weixin, WeiboPublisher, \
    Weibo, ArticlePublisher, Article, Topic, TopicArticles, TopicWeibo, \
    TopicWeixin, RelatedData, RelateddataArticles, RelateddataWeibo, \
    RelateddataWeixin, ArticleCategory, ArticleCategoryArticles, \
    CustomArticle, Custom, CustomWeixin, CustomWeibo, Keyword, Inspection
from peewee import *


def save_article_publisher(data):
    article_publisher = ArticlePublisher(
        publisher=data["publisher"],
        searchmode=data.get("searchmode", 0)
    )
    article_publisher.save()

    return article_publisher


def save_weixin_publisher(data):
    weixin_publisher = WeixinPublisher(
        publisher = data["publisher"]
    )
    weixin_publisher.save()

    return weixin_publisher


def save_weibo_publisher(data):
    weibo_publisher = WeiboPublisher(
        publisher = data["publisher"]
    )
    weibo_publisher.save()

    return weibo_publisher


def save_article(data):
    article = Article(
        author=data["author"],
        title=data["title"],
        url=data["url"],
        content=data["content"],
        source=data["source"],
        pubtime=fromtimestamp(data["pubtime"]),    
        publisher=data["publisher"],
        area=data["area"],
        uuid=data["id"],
        website_type=data["type"]
    )
    article.save()

    return article


def save_weixin(data):
    weixin = Weixin(
        author=data["author"],
        title=data["title"],
        url=data["url"],
        content=data["content"],
        origin_source=data["origin_source"],
        source=data["source"],
        website_type=data["type"],
        pubtime=fromtimestamp(data["pubtime"]),
        publisher=data["publisher"],
        area=get_area(data["province"], data["city"], data["district"]),
        uuid=data["id"]
    )
    weixin.save()

    return weixin


def save_weibo(data):
    weibo = Weibo(
        author=data["author"],
        title=data["title"],
        url=data["url"],
        content=data["content"],
        origin_source=data["origin_source"],
        source=data["source"],
        website_type=data["type"],
        pubtime=fromtimestamp(data["pubtime"]),
        publisher=data["publisher"],
        area=get_area(data["province"], data["city"], data["district"]),
        attitudes_count = data["attitudes_count"],
        comments_count = data["comments_count"],
        reposts_count = data["reposts_count"],
        uuid=data["id"]
    )
    weibo.save()

    return weibo


def save_custom(data):
    custom = Custom(
        searchkeyword=data["key"]
    )
    custom.save()
    return custom


def save_topic_article(data, article):
    topic_article = TopicArticles(
        topic=get_topic(data["key"]),
        article=article
    )
    topic_article.save()

    return topic_article


def save_custom_article(data, article, custom):
    custom_article = CustomArticle(
        custom=custom,
        article=article
    )
    custom_article.save()

    return custom_article

def save_topic_weixin(data, weixin):
    topic_weixin = TopicWeixin(
        topic=get_topic(data["key"]),
        weixin=weixin
    )
    topic_weixin.save()

    return topic_weixin


def save_custom_weixin(data, weixin):
    custom_weixin = CustomWeixin(
        custom=get_custom(data["key"]),
        weixin=weixin
    )
    custom_weixin.save()

    return custom_weixin


def save_custom_weibo(data, weibo):
    custom_weibo = CustomWeibo(
        custom=get_custom(data["key"]),
        weibo=weibo
    )
    custom_weibo.save()

    return custom_weibo


def save_topic_weibo(data, weibo):
    topic_weibo = TopicWeibo(
        topic=get_topic(data["key"]),
        weibo=weibo
    )
    topic_weibo.save()

    return topic_weibo


def save_article_category_articles(data, article, category):
    article_category_articles = ArticleCategoryArticles(
        articlecategory=get_article_category(category),
        article=article
    )
    article_category_articles.save()

    return article_category_articles


def save_relateddata(data):
    relateddata = RelatedData(
        uuid=data["id"]
    )
    relateddata.save()

    return relateddata


def save_relateddata_articles(relateddata, article):
    relateddata_articles = RelateddataArticles(
        relateddata=relateddata,
        article=article
    )
    relateddata_articles.save()

    return relateddata_articles


def save_relateddata_weixin(relateddata, weixin):
    relateddata_weixin = RelateddataWeixin(
        relateddata=relateddata,
        weixin=weixin
    )
    relateddata_weixin.save()

    return relateddata_weixin


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


def get_area_by_name(name):
    return (Area
            .select()
            .where(
                (Area.name == name) &
                (Area.level != 1))
            .order_by(Area.level.asc()))


def get_area(province=None, city=None, district=None):
    """
    Get Single Area Instance
    """

    if province and city and district:
        area = Area.select().where(Area.name == district)

        if area.count() == 1:
            return area[0]

        if area.count() > 1:
            for a in area:
                name = Area.get(
                    Area.id == Area.get(
                        Area.id == Area.get(
                            Area.name == district
                        ).parent_id
                    ).parent_id
                ).name

                if name == province:
                    return a

    if province and city:
        area = Area.select().where(Area.name == city)

        if area.count() == 1:
            return area[0]

        if area.count() > 1:
            for a in area:
                name = Area.get(
                    Area.id == Area.get(
                        Area.name == city
                    ).parent_id
                ).name

                if name == province:
                    return a

    if province:
        area = Area.select().where(Area.name == province)

        return area

    if not province:
        return Area.select().where(Area.name == u"全国")


def get_article_publisher(publisher):
    return ArticlePublisher.get(
        ArticlePublisher.publisher == publisher)


def get_weixin_publisher(publisher):
    return WeixinPublisher.get(
        WeixinPublisher.publisher == publisher)


def get_weibo_publisher(publisher):
    return WeiboPublisher.get(
        WeiboPublisher.publisher == publisher)


def get_relateddata(uuid):
    """
    Get Single RelatedData Instance
    """
    return RelatedData.get(RelatedData.uuid == uuid)


def get_article_category(category):
    """
    Get Single ArticleCategory Instance
    """
    return ArticleCategory.get(ArticleCategory.name == category)


def get_topic(title):
    """
    Get Single Topic Instance
    """
    return Topic.get(Topic.title == title)


def get_custom(searchkeyword):
    """
    Get Single Custom Instance
    """
    return Custom.get(Custom.searchkeyword == searchkeyword)


def get_article(uuid):
    """
    Get Single Article Instance
    """
    return Article.get(Article.uuid == uuid)


def get_weixin(uuid):
    return Weixin.get(Weixin.uuid == uuid)


def get_weibo(uuid):
    return Weibo.get(Weibo.uuid == uuid)


def get_muti_article(pubtime, interval):
    """
    Select from MySQL
    Get muti data

    pubtime: datetime
    interval: days
    """
    return Article.select().where(
        (Article.pubtime < pubtime) & 
        (Article.pubtime > pubtime - timedelta(days=7)))


def get_muti_weixin(pubtime, interval):
    """
    Select from MySQL
    Get muti data

    pubtime: datetime
    interval: days
    """
    return Weixin.select().where(
        (Weixin.pubtime < pubtime) & 
        (Weixin.pubtime > pubtime - timedelta(days=7)))


def get_muti_weibo(pubtime, interval):
    """
    Select from MySQL
    Get muti data

    pubtime: datetime
    interval: days
    """
    return Weibo.select().where(
        (Weibo.pubtime < pubtime) & 
        (Weibo.pubtime > pubtime - timedelta(days=7)))


def get_inspectionMaxID():
    """
    Get Single inspection max id Instance
    """
    return Inspection.select(fn.Max(Inspection.id)).scalar()


def paginate_article(page, count):
    return Article.select().where(Article.feeling_factor == -1).paginate(page, count)


def count():
    return Article.select().where(Article.feeling_factor == -1).count()


def article_publisher_count(publisher):
    return ArticlePublisher.select().where(ArticlePublisher.publisher == publisher).count()


def weixin_publisher_count(publisher):
    return WeixinPublisher.select().where(WeixinPublisher.publisher == publisher).count()


def weibo_publisher_count(publisher):
    return WeiboPublisher.select().where(WeiboPublisher.publisher == publisher).count()


def relateddata_count(uuid):
    return RelatedData.select().where(RelatedData.uuid == uuid).count()


def custom_count(searchkeyword):
    return Custom.select().where(Custom.searchkeyword == searchkeyword).count()


def update_keyword(custom, data):
    keyword = Keyword.update(custom=custom, review='').where(Keyword.review ==data['key'])
    keyword.execute()
    return keyword
