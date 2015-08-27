import requests
from urllib import quote,unquote

urlx = 'http://www.kjson.com/weixin/api?key=7772634ceb2d264111061463b27e499d'
url = 'http://mp.weixin.qq.com/s?__biz=MjM5NzMxNjc4OA==&mid=207755817&idx=1&sn=461dfb23f1a8b4847412f7193611385a&3rd=MzA3MDU4NTYzMw==&scene=6#rd'
# aa =requests.post(urlx,data={'urls':url})
# print aa.text

t = 'uin=MTI4ODc3MTMyMg%3D%3D&key=1936e2bc22c2ceb57ed009627fb4a926de66e97caa7cef7a4e600ce9dd1dfbe38f5cc883723ebd9c5f05f7b30cac8b27&pass_ticket=K4vllwRR4MAmE5Bv3F4HDV576xatPYNYS9Tu1qFa4jsjGafvoe81ZB2usfgm0sz'
print unquote(t)
# data = {
#     'uin': 'MTI4ODc3MTMyMg==',
#     'key': '2e5b2e802b7041cfafa9d327fd0197a007e02d90d947cf560d8712b884e9b0347dc548eb712259bafe45d9df766ca1c1',
#     'pass_ticket': 'drQta4qOF5b03nbGc13aH60o36qBk9fIugOhK7s1n2ccD7n1YD2ltXWnHVRbIo0E',
#     '__biz': 'MjM5ODA3NTg3Mg==',
#     'f': 'json',
#     'devicetype': 'android-15',
#     'is_need_ad': 1,
#     'comment_id': 0,
#     'is_need_reward': 0,
#     'reward_uin_count': 0
# }
# t = '?uin=MTI4ODc3MTMyMg==&key=2e5b2e802b7041cfafa9d327fd0197a007e02d90d947cf560d8712b884e9b0347dc548eb712259bafe45d9df766ca1c1'
# url = url+t
# bb = requests.post(url,data=data)
# print bb.text
# url = 'http://mp.weixin.qq.com/s?__biz=MjM5ODA3NTg3Mg==&mid=463713477&idx=2&sn=7b048193245316a56d7a96cfba6d5e11&key=2e5b2e802b7041cfafa9d327fd0197a007e02d90d947cf560d8712b884e9b0347dc548eb712259bafe45d9df766ca1c1&ascene=7&uin=MTI4ODc3MTMyMg%3D%3D&devicetype=android-15&version=2601004a&nettype=WIFI&pass_ticket=drQta4qOF5b03nbGc13aH60o36qBk9fIugOhK7s1n2ccD7n1YD2ltXWnHVRbIo0E'
# cc = requests.get(url)
# print cc

# url = "http://mp.weixin.qq.com/s?__biz=MjM5NDg5NzI1NQ==&mid=205197958&idx=1&sn=06077a2bd7d6ab94a8f1e03761a43142&3rd=MzA3MDU4NTYzMw==&scene=6#rd"
# aa =  requests.options(url)
# print aa.headers