# -*- coding: utf-8 -*-
import requests
from urllib import quote ,unquote

url = 'http://mp.weixin.qq.com/mp/getappmsgext?__biz=MjM5ODA3NDc0MA==&mid=204593366&idx=7&scene=2&title=%E4%BB%9671%E5%B2%81%E5%85%A5%E7%8B%B1%EF%BC%8C85%E5%B2%81%E8%BA%AB%E5%AE%B6%E8%BF%87%E4%BA%BF%EF%BC%81&ct=1427367580&devicetype=android-15&version=&f=json&r=0.3372718470636755&is_need_ad=1&comment_id=0&is_need_reward=0&reward_uin_count=0&uin=MTI4ODc3MTMyMg%3D%3D&key=1936e2bc22c2ceb57ed009627fb4a926de66e97caa7cef7a4e600ce9dd1dfbe38f5cc883723ebd9c5f05f7b30cac8b27&pass_ticket=K4vllwRR4MAmE5Bv3F4HDV576xatPYNYS9Tu1qFa4jsjGafvoe81ZB2usfgm0szw'
# url = 'http://mp.weixin.qq.com/mp/getappmsgext?__biz=MjM5NTQ0OTU1MQ==&mid=205388219&idx=7&scene=2&title=%E4%BB%9671%E5%B2%81%E5%85%A5%E7%8B%B1%EF%BC%8C85%E5%B2%81%E8%BA%AB%E5%AE%B6%E8%BF%87%E4%BA%BF%EF%BC%81&ct=1427367580&devicetype=android-15&version=&f=json&r=0.3372718470636755&is_need_ad=1&comment_id=0&is_need_reward=0&reward_uin_count=0&uin=MTI4ODc3MTMyMg==&key=7772634ceb2d264111061463b27e499d&pass_ticket=mmXdnUpwMC4%2B1nDD4mLyVBYHvjmfbjkUvaTiLcFnQaZW4gS8Klwmog6iW7swBCgl'
# print unquote(url)
# url = "http://mp.weixin.qq.com/mp/getappmsgext?__biz=MjM5ODA3NDc0MA==&mid=204593366&idx=2&scene=2&title=%E4%B8%80%E4%B8%AA%E5%86%9C%E6%9D%91%E5%A5%B3%E5%AD%A9%E7%9A%84%E7%8B%AC%E7%99%BD%EF%BC%9A%E4%B8%8A%E5%A4%A7%E5%AD%A6%E6%9C%89%E4%BB%80%E4%B9%88%E7%94%A8%EF%BC%9F&ct=1428843571&devicetype=android-15&version=&f=json&r=0.4801011618692428&is_need_ad=0&comment_id=0&is_need_reward=0&reward_uin_count=0&uin=MTI4ODc3MTMyMg%3D%3D&key=2e5b2e802b7041cfed13c42a4d8f20bd399e8f7c1fdb98034c1e13ad4991b9585829254a33fe11914fe1d10b224e5245&pass_ticket=mmXdnUpwMC4%252B1nDD4mLyVBYHvjmfbjkUvaTiLcFnQaZW4gS8Klwmog6iW7swBCgl"
# url = "http://mp.weixin.qq.com/s?__biz=MjM5MzEyODcyNw==&mid=232216491&idx=1&sn=d9160a25fa461ca84731dbf962a58e09&3rd=MzA3MDU4NTYzMw==&scene=6#rd"
# print unquote(url)
# my_referer = "http://mp.weixin.qq.com/s?__biz=MzA5NzgyNTMxMQ==&mid=206908827&idx=1&sn=71aea6109c152e76c0635d7acda8830e&scene=2&from=timeline&isappinstalled=0&key=2e5b2e802b7041cf8066a5e7da6785392ba2076b1f1221ebc0859e5b44f924c276cb991580c59eed69ca49238006fcca&ascene=2&uin=MTI4ODc3MTMyMg%3D%3D&devicetype=android-15&version=2601004a&nettype=WIFI&pass_ticket=mmXdnUpwMC4%2B1nDD4mLyVBYHvjmfbjkUvaTiLcFnQaZW4gS8Klwmog6iW7swBCgl"
# url = 'http://mp.weixin.qq.com/s?__biz=MjM5MzEyODcyNw==&mid=232216491&idx=1&sn=d9160a25fa461ca84731dbf962a58e09&3rd=MzA3MDU4NTYzMw==&scene=6#rd'
# print unquote(url)
cookies = {
    'pgv_pvid': '5281704024'
}
UA2 = "QV=2&PL=ADR&PR=TBS&PB=GE&VE=B1&VN=1.0.1.0002&CO=X5&COVN=025411&RF=PRI&PP=com.tencent.mm&PPVC=2601004a&RL=540*960&MO= HUAWEIT8950 &DE=PHONE&OS=4.0.4&API=15&CHID=11111&LCID=9422"
GUID = "e79612fc07381fc556552e29377988cb"
Auth = "31045b957cf33acf31e40be2f3e71c5217597676a9729f1b"
s = requests.Session()
#s.headers.update({'referer': my_referer})
# s.headers.update({'cookies': cookies})
s.headers.update({'Q-UA2': UA2})
s.headers.update({'Q-GUID': GUID})
s.headers.update({'Q-Auth': Auth})
s.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.4; zh-cn; HUAWEI T8950 Build/HuaweiT8950) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025411 Mobile Safari/533.1 MicroMessenger/6.1.0.74_r1098891.543 NetType/WIFI'})

r = s.get(url)
print r.content


# url = 'http://mp.weixin.qq.com/s?__biz=MjM5MzEyODcyNw==&mid=232216491&idx=1&sn=d9160a25fa461ca84731dbf962a58e09&3rd=MzA3MDU4NTYzMw==&scene=6#rd'
# aa =  requests.get(url)
# print aa.headers
