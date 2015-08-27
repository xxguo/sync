# -*- coding: utf-8 -*-
import re
import math

import jieba
import jieba.analyse

import nltk
from numpy import array

from connection import get_session, close_session
from cassandra.query import dict_factory


def compare(a, b, id):

    a1 = [x for x in a]
    b1 = [x for x in b]

    union = list(set(a1).union(set(b1)))

    a_count = [a1.count(x) for x in union]
    b_count = [b1.count(x) for x in union]

    print tuple(a_count)

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

    # if value > 0.9:
    print id, value
    # print math.acos(value) * 180 / math.pi


def cal_weight(session):
    session.set_keyspace('zjld')
    session.row_factory = dict_factory
    rows = session.execute("SELECT id, comment from article")
    for row in rows:
        text = list(row.get('comment').values())[0]
        tags = jieba.analyse.extract_tags(text, topK=50, withWeight=True)
        if len(tags) < 50:
            continue
        session.execute("INSERT INTO words_weight (id, weight) VALUES (%s, %s)", [row.get('id'), [tag[1] for tag in tags]])


def get_weight(session):
    session.set_keyspace('zjld')
    session.row_factory = dict_factory
    rows = session.execute("SELECT weight from words_weight")
    datas = [array(v) for v in [row['weight'] if row['weight'] and len(row['weight']) >= 10 else [] for row in rows]]
    return datas


def gaac(datas=[]):
    # datas = [array(v) for v in [(1,0),(0,1),(1,1),(5,5),(5,4),(4,5,6)]]

    """
    Kmeans聚类
    """
    km = nltk.cluster.kmeans.KMeansClusterer(num_means=10, distance=nltk.cluster.util.euclidean_distance)
    km.cluster(vectors=datas)
    for data in datas:
        print str(data) + str(km.classify(data))

    """
    GAAC聚类,距离使用的是点积的结果
    """
    # ga = nltk.cluster.gaac.GAAClusterer(num_clusters=10, normalise=False)
    # ga.cluster(vectors=datas)

    """
    混合高斯聚类
    """
    # emc = nltk.cluster.em.EMClusterer(initial_means=[[4, 2], [4, 2.01]])
    # emc.cluster(vectors=datas)

    # for data in datas:
    #     print str(data) + str(emc.classify(data))


if __name__ == '__main__':

    # session = get_session()
    # cal_weight(session)
    # gaac(get_weight(session))

    # rows = session.execute("SELECT id, comment FROM article")
    # for row in rows:
    #     word = list(row.get('comment').values())[0].encode('utf-8')
    #     a = jieba.cut(u" 　　日前，质检总局公布了采暖散热器产品质量国家监督抽查报告。报告显示，螺纹精度不合格成为产品主要不合格项目之一。螺纹精度在采暖散热器产品中起什么作用，为何会出现不合格，不合格产品会给消费者带来哪些危害？中国质量报记者就此采访了国家散热器质检中心工程师齐嘉卉。　　齐嘉卉告诉中国质量报记者，螺纹精度是所有供暖设施和采暖散热器中都会涉及到的项目之一，主要是指散热器两侧与管路连接处的螺纹口部位，其质量和加工精度称为螺纹精度。因为涉及到散热器产品与管路的连接，所以通常螺纹连接的紧密程度直接关系到正常使用中散热器产品的安全性，是仅次于散热量和水压两个关键项之外的重要项目。散热器管路本身是有压力的，如果螺纹连接的部位不够好，一旦管路进行正常供暖后，就会发生慢速渗漏等漏水的情况，如果压力过大，会发生接口处爆裂的情况，带来相当严重的后果。　　“螺纹精度不合格最主要的表现就是通规不通，止规不止，也就是螺纹跟散热器其他配件适配的时候有可能过大或者过小，连接起来过紧或过松。”齐嘉卉说，由于国内目前已经禁止使用胶垫，出现螺纹口过大的情况时，在散热器安装过程中一般会填充一些生料带或者其他填充物，但是生料带是有使用年限的，到一定的年限后生料带会产生物理反应和化学反应，造成生料带直接进入循环管路中，造成管路的堵塞，最终引发水管发生渗漏或者爆裂，这种情况屡见不鲜。若螺纹口过小，则会导致跟散热器连接时拧不进去，因为螺纹口的连接处是铜管，如果用蛮力去拧螺纹口的话，会导致其变形，目前很多散热器材质是铝合金等软材质，尤其是钢铝复合的材质，会导致散热量和使用安全性受到直接影响。　　既然螺纹精度如此重要，那为何目前仍未纳入强制性国标的范畴？齐嘉卉告诉中国质量报记者，目前直接涉及螺纹精度的3个标准中，有2个是国家推荐性标准，一个是行业推荐性标准，从2000年左右就已开始实施，但标准的制修订或者实时更新等情况并不乐观。且上述3个螺纹精度标准中只有一个是针对采暖散热器产品的，另外2个针对所有机械加工行业，但3个标准在采暖散热器行业中都有执行。更显混乱的是，在与采暖散热器相关的19个标准中，强制性标准规定的强制性条款只有一条，即水压试验项目，其他的规定完全是企业根据实际情况执行，自主性较大。　　“每年抽检都会反映出螺纹精度标准混乱的情况，但目前来看还没有比较明确或者实用的办法来解决这个问题。”齐嘉卉说，采暖散热器行业所有的螺纹部件基本上都是外购外协的（企业和厂家直接协商采购），企业的生产过程只限于散热器本身，即按照工艺流程，直接对部件进行焊接，组装出散热器成品。　　“目前在行业相关部门和标准制修订部门没有很好解决措施的情况下，只能靠企业自主的行为，严把进货关，对配件质量进行严格检验把关，才能最大限度避免成品出现问题。”齐嘉卉说，因为散热器行业属于整个机械加工行业中的一个规模较小的分支产业，因此要实行统一标准涉及因素太多，难度很大，但鉴于目前存在的诸多问题，相关部门仍应给予积极的关注，并尽快出台可行的解决措施。　　“整体来说，目前散热器产品包括铸铁、钢、铝、压铸铝合金、复合型等多种型式，行业仍旧比较混乱。”针对采暖散热器产品类型多、质量问题多发的情况，齐嘉卉表示，消费者在购买之前要尽量查看产品此前的国家监督抽查报告或其他相关信息，然后和有意向产品进行详细对照，再进行实际采购。　　“根据实际的抽查情况看，很多企业的宣传都名不副实。”齐嘉卉说，有些企业在网上可搜索到的信息和荣誉都很多，但这种类型的企业80%都名不副实，消费者在选购时不要只看价格。虽然散热器产品外表都差不多，加工等细节看不出来，但内在有很大的区别，比如钢制散热器，壁厚是一个很大的卖点，壁厚超过2cm的产品比壁厚小于2cm的产品使用寿命相对要长1~2年，在壁厚小于1.5cm的情况下，有时候产品寿命可能只有一个采暖季。散热器出现问题时，不止自家受影响，还会牵扯到邻里，甚至出现法律纠纷，因此安装时一定要选购质量过硬的产品。")
    #     b = jieba.cut(u" 　　日前，质检总局公布了采暖散热器产品质量国家监督抽查报告。报告显示，螺纹精度不合格成为产品主要不合格项目之一。螺纹精度在采暖散热器产品中起什么作用，为何会出现不合格，不合格产品会给消费者带来哪些危害？中国质量报记者就此采访了国家散热器质检中心工程师齐嘉卉。　　齐嘉卉告诉中国质量报记者，螺纹精度是所有供暖设施和采暖散热器中都会涉及到的项目之一，主要是指散热器两侧与管路连接处的螺纹口部位，其质量和加工精度称为螺纹精度。因为涉及到散热器产品与管路的连接，所以通常螺纹连接的紧密程度直接关系到正常使用中散热器产品的安全性，是仅次于散热量和水压两个关键项之外的重要项目。散热器管路本身是有压力的，如果螺纹连接的部位不够好，一旦管路进行正常供暖后，就会发生慢速渗漏等漏水的情况，如果压力过大，会发生接口处爆裂的情况，带来相当严重的后果。　　“螺纹精度不合格最主要的表现就是通规不通，止规不止，也就是螺纹跟散热器其他配件适配的时候有可能过大或者过小，连接起来过紧或过松。”齐嘉卉说，由于国内目前已经禁止使用胶垫，出现螺纹口过大的情况时，在散热器安装过程中一般会填充一些生料带或者其他填充物，但是生料带是有使用年限的，到一定的年限后生料带会产生物理反应和化学反应，造成生料带直接进入循环管路中，造成管路的堵塞，最终引发水管发生渗漏或者爆裂，这种情况屡见不鲜。若螺纹口过小，则会导致跟散热器连接时拧不进去，因为螺纹口的连接处是铜管，如果用蛮力去拧螺纹口的话，会导致其变形，目前很多散热器材质是铝合金等软材质，尤其是钢铝复合的材质，会导致散热量和使用安全性受到直接影响。　　既然螺纹精度如此重要，那为何目前仍未纳入强制性国标的范畴？齐嘉卉告诉中国质量报记者，目前直接涉及螺纹精度的3个标准中，有2个是国家推荐性标准，一个是行业推荐性标准，从2000年左右就已开始实施，但标准的制修订或者实时更新等情况并不乐观。且上述3个螺纹精度标准中只有一个是针对采暖散热器产品的，另外2个针对所有机械加工行业，但3个标准在采暖散热器行业中都有执行。更显混乱的是，在与采暖散热器相关的19个标准中，强制性标准规定的强制性条款只有一条，即水压试验项目，其他的规定完全是企业根据实际情况执行，自主性较大。　　“每年抽检都会反映出螺纹精度标准混乱的情况，但目前来看还没有比较明确或者实用的办法来解决这个问题。”齐嘉卉说，采暖散热器行业所有的螺纹部件基本上都是外购外协的（企业和厂家直接协商采购），企业的生产过程只限于散热器本身，即按照工艺流程，直接对部件进行焊接，组装出散热器成品。　　“目前在行业相关部门和标准制修订部门没有很好解决措施的情况下，只能靠企业自主的行为，严把进货关，对配件质量进行严格检验把关，才能最大限度避免成品出现问题。”齐嘉卉说，因为散热器行业属于整个机械加工行业中的一个规模较小的分支产业，因此要实行统一标准涉及因素太多，难度很大，但鉴于目前存在的诸多问题，相关部门仍应给予积极的关注，并尽快出台可行的解决措施。　　“整体来说，目前散热器产品包括铸铁、钢、铝、压铸铝合金、复合型等多种型式，行业仍旧比较混乱。”针对采暖散热器产品类型多、质量问题多发的情况，齐嘉卉表示，消费者在购买之前要尽量查看产品此前的国家监督抽查报告或其他相关信息，然后和有意向产品进行详细对照，再进行实际采购。　　“根据实际的抽查情况看，很多企业的宣传都名不副实。”齐嘉卉说，有些企业在网上可搜索到的信息和荣誉都很多，但这种类型的企业80%都名不副实，消费者在选购时不要只看价格。虽然散热器产品外表都差不多，加工等细节看不出来，但内在有很大的区别，比如钢制散热器，壁厚是一个很大的卖点，壁厚超过2cm的产品比壁厚小于2cm的产品使用寿命相对要长1~2年，在壁厚小于1.5cm的情况下，有时候产品寿命可能只有一个采暖季。散热器出现问题时，不止自家受影响，还会牵扯到邻里，甚至出现法律纠纷，因此安装时一定要选购质量过硬的产品。")
    #     # b = jieba.cut(word)
    #     compare(a, b, row.get('id'))
    #     break

    # session.cluster.shutdown()
    # compare(jieba.cut(extract(u"我喜欢看电视，不喜欢看电影")), jieba.cut(extract(u"我不喜欢看电视，也不喜欢看电影")))