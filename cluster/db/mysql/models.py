# -*- coding: utf-8 -*-

from peewee import *
from db.mysql.connection import mysql_db_pool


class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db_pool()


class Area(BaseModel):
    name = CharField(max_length=255, verbose_name=u'名称')
    level = BigIntegerField(null=False, verbose_name=u'等级')
    parent_id = IntegerField()

    class Meta:
        db_table = 'area'
        verbose_name_plural = u'地域'

    def __unicode__(self):
        return self.name


class WeixinPublisher(BaseModel):
    photo = TextField(default='', verbose_name=u'用户头像')
    publisher = CharField(max_length=255, verbose_name=u'发布者')
    brief = CharField(default='', max_length=255, verbose_name=u'简介')

    class Meta:
        db_table = 'weixinpublisher'
        verbose_name_plural = u'微信发布者'

    def __unicode__(self):
        return self.publisher


class Weixin(BaseModel):
    author = CharField(max_length=255, verbose_name=u'作者')
    title = CharField(max_length=255, verbose_name=u'标题')
    url = TextField(verbose_name=u'网站链接')
    content = TextField(verbose_name=u'正文')
    origin_source = CharField(max_length=255, verbose_name=u'信息转载来源')
    source = CharField(max_length=255,  verbose_name=u'信息来源')
    website_type = CharField(max_length=255,  verbose_name=u'网站类型', default='gov')
    pubtime = DateTimeField(verbose_name=u'发布时间')
    publisher = ForeignKeyField(WeixinPublisher, verbose_name=u'微信发布者')
    area = ForeignKeyField(Area, verbose_name=u'名称')
    uuid = CharField(max_length=36)
    likenum = IntegerField(default=0)
    readnum = IntegerField(default=0)

    class Meta:
        db_table = 'weixin'
        verbose_name_plural = u'微信'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class WeiboPublisher(BaseModel):
    photo = TextField(default='', verbose_name=u'用户头像')
    publisher = CharField(max_length=255, verbose_name=u'发布者')
    brief = CharField(default='', max_length=255, verbose_name=u'简介')

    class Meta:
        db_table = 'weibopublisher'
        verbose_name_plural = u'微博发布者'

    def __unicode__(self):
        return self.publisher


class Weibo(BaseModel):
    author = CharField(max_length=255, verbose_name=u'作者')
    title = CharField(max_length=255, verbose_name=u'标题')
    url = TextField(verbose_name=u'网站链接')
    content = TextField( verbose_name=u'正文')
    origin_source = CharField(max_length=255,  verbose_name=u'信息转载来源')
    source = CharField(max_length=255,  verbose_name=u'信息来源')
    website_type = CharField(max_length=255,  verbose_name=u'网站类型', default='gov')
    pubtime = DateTimeField(verbose_name=u'发布时间')
    publisher = ForeignKeyField(WeiboPublisher, verbose_name=u'微博发布者')
    area = ForeignKeyField(Area, verbose_name=u'名称')
    attitudes_count = IntegerField(default=0, verbose_name=u'点赞数')
    comments_count = IntegerField(default=0, verbose_name=u'评论量')
    reposts_count = IntegerField(default=0, verbose_name=u'转发量')
    uuid = CharField(max_length=36)

    class Meta:
        db_table = 'weibo'
        verbose_name_plural = u'微博'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class ArticlePublisher(BaseModel):
    photo = TextField(default='', verbose_name=u'用户头像')
    publisher = CharField(max_length=255, verbose_name=u'发布者')
    brief = CharField(default='', max_length=255, verbose_name=u'简介')
    searchmode = IntegerField(default=0)

    class Meta:
        db_table = 'articlepublisher'
        verbose_name_plural = u'文章发布者'

    def __unicode__(self):
        return self.publisher


class Article(BaseModel):
    author = CharField(max_length=255, verbose_name=u'作者')
    title = CharField(max_length=255, verbose_name=u'标题')
    url = TextField(verbose_name=u'网站链接')
    content = TextField( verbose_name=u'正文')
    source = CharField(max_length=255,  verbose_name=u'信息来源')
    pubtime = DateTimeField(verbose_name=u'发布时间')
    publisher = ForeignKeyField(ArticlePublisher, verbose_name=u'文章发布者')
    area = ForeignKeyField(Area, verbose_name=u'名称')
    uuid = CharField(max_length=36)
    feeling_factor = FloatField(default=-1, verbose_name=u"正负面")
    website_type = CharField(max_length=36, default='gov')

    class Meta:
        db_table = 'article'
        verbose_name_plural = u'文章'
        ordering = ['-pubtime']

    def __unicode__(self):
        return self.title


class Topic(BaseModel):
    title = CharField(max_length=255, verbose_name=u'标题')
    abstract = TextField( verbose_name=u'正文')

    class Meta:
        db_table = 'topic'
        verbose_name_plural = u'聚类事件'

    def __unicode__(self):
        return self.title


class TopicArticles(BaseModel):
    """
    Table: Topic
    Table: Article
    ManyToMany
    """
    
    topic = ForeignKeyField(Topic)
    article = ForeignKeyField(Article)

    class Meta:
        db_table = 'topic_articles'


class Custom(BaseModel):
    searchkeyword = CharField(max_length=255, verbose_name=u'标题')

    class Meta:
        db_table = 'custom'
        verbose_name_plural = u'指定监测'

    def __unicode__(self):
        return self.keyword


class Keyword(BaseModel):
    newkeyword = CharField(max_length=255, verbose_name=u'关键词')
    review = CharField(max_length=255, default=u'', verbose_name=u'审核')
    custom = ForeignKeyField(Custom)

    class Meta:
        db_table = 'keyword'
        verbose_name_plural = u'关键词'

    def __unicode__(self):
        return self.newkeyword    


class CustomArticle(BaseModel):
    """
    Table: Custom
    Table: Article
    ManyToMany
    """

    custom = ForeignKeyField(Custom)
    article = ForeignKeyField(Article)

    class Meta:
        db_table = 'custom_articles'


class CustomWeixin(BaseModel):
    """
    Table: Custom
    Table: Weixin
    ManyToMany
    """    

    custom = ForeignKeyField(Custom)
    weixin = ForeignKeyField(Weixin)

    class Meta:
        db_table = 'custom_weixin'


class CustomWeibo(BaseModel):
    """
    Table: Custom
    Table: Weibo
    ManyToMany
    """    

    custom = ForeignKeyField(Custom)
    weibo = ForeignKeyField(Weibo)

    class Meta:
        db_table = 'custom_weibo'


class TopicWeibo(BaseModel):
    """
    Table: Topic
    Table: Weibo
    ManyToMany
    """

    topic = ForeignKeyField(Topic)
    weibo = ForeignKeyField(Weibo)

    class Meta:
        db_table = 'topic_weibo'


class TopicWeixin(BaseModel):
    """
    Table: Topic
    Table: Weixin
    ManyToMany
    """

    topic = ForeignKeyField(Topic)
    weixin = ForeignKeyField(Weixin)

    class Meta:
        db_table = 'topic_weixin'


class RelatedData(BaseModel):
    uuid = CharField(max_length=36, verbose_name=u'uuid')

    class Meta:
        db_table = 'relateddata'
        verbose_name_plural = u'关联文章'

    def __unicode__(self):
        return self.uuid


class RelateddataArticles(BaseModel):
    """
    Table: RelatedData
    Table: Article
    ManyToMany
    """

    relateddata = ForeignKeyField(RelatedData)
    article = ForeignKeyField(Article)

    class Meta:
        db_table = 'relateddata_articles'


class RelateddataWeibo(BaseModel):
    """
    Table: RelatedData
    Table: Weibo
    ManyToMany
    """

    relateddata = ForeignKeyField(RelatedData)
    weibo = ForeignKeyField(Weibo)

    class Meta:
        db_table = 'relateddata_weibo'


class RelateddataWeixin(BaseModel):
    """
    Table: RelatedData
    Table: Weixin
    ManyToMany
    """

    relateddata = ForeignKeyField(RelatedData)
    weixin = ForeignKeyField(Weixin)

    class Meta:
        db_table = 'relateddata_weixin'


class ArticleCategory(BaseModel):
    name = CharField(max_length=255,  verbose_name=u'')
    remark = CharField(max_length=255,  verbose_name=u'备注')

    class Meta:
        db_table = 'article_category'
        verbose_name_plural = u'文章分类'


class ArticleCategoryArticles(BaseModel):
    """
    Table: ArticleCategory
    Table: Article
    ManyToMany
    """

    articlecategory = ForeignKeyField(ArticleCategory)
    article = ForeignKeyField(Article)

    class Meta:
        db_table = 'article_category_articles'

class Inspection(BaseModel):
    id = IntegerField( primary_key=True, verbose_name=u'编号')
    url = CharField(max_length=255, verbose_name=u'网站链接')
    name = CharField(max_length=255, verbose_name=u'名称')
    manufacturer = CharField(max_length=255, null=True,verbose_name=u'转载次数')
    qualitied = FloatField(verbose_name=u'关注度',null=True)
    pubtime = DateTimeField(verbose_name=u'发布时间')
    product = CharField(max_length=255, verbose_name=u'名称')
    source = CharField(max_length=255, verbose_name=u'信息来源')
    province = CharField(max_length=255, verbose_name=u'省')
    city = CharField(max_length=255, null=True, verbose_name=u'市')
    district = CharField(max_length=255, null=True, verbose_name=u'地区')
    create_at = DateTimeField(verbose_name=u'发布时间')
    update_at = DateTimeField(verbose_name=u'发布时间')

    class Meta:
        db_table = 'inspection'
        verbose_name_plural = u'抽检'
        # ordering = ['-pubtime']

    def __unicode__(self):
        return self.id
