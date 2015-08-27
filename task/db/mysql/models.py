# -*- coding: utf-8 -*-

from peewee import *
from db.mysql.connection import mysql_db


class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db()


class Topic(BaseModel):
    title = CharField(max_length=255, verbose_name=u'标题')
    abstract = TextField( verbose_name=u'正文')

    class Meta:
        db_table = 'topic'
        verbose_name_plural = u'聚类事件'

    def __unicode__(self):
        return self.title


class Keyword(BaseModel):
    newkeyword = CharField(max_length=255, verbose_name=u'关键词')
    review = CharField(max_length=255, default=u'', verbose_name=u'审核')
    #synced = models.CharField(max_length=255, default=u'', verbose_name=u'同步')
    # group = models.ForeignKey(Group)
    # custom = models.ForeignKey(Custom)
    class Meta:
        db_table = 'keyword'
        verbose_name_plural = u'关键词'

    def __unicode__(self):
        return self.review


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
