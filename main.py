# -*- encoding:utf8 -*-
import os
import sys
from scrapy.cmdline import execute

# 调用scrapy的函数execute进行运行测试

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# scrapy crawl douban
execute(["scrapy", "crawl", "douban"])


# one = set()
# words = {"tokens":[{"token":"sadasd"}, {"token":"45"}, {"token":"45"}]}
# print(set([r["token"] for r in words["tokens"] if len(r["token"]) > 1]))

# 静态方法
"""
class Test(object):
    @classmethod
    def test(cls, one):
        print("testst-"+one)


test = Test()
test.test(one="45455454")

Test.test(one="1111111111")
"""

# 抽象类
'''
from abc import ABCMeta, abstractmethod, ABC


class Foo(ABC):
    @abstractmethod
    def fun(self):
        """
        你需要在子类中实现该方法, 子类才允许被实例化
        :return
        """

    @abstractmethod
    def fun1(self):
        print("11111111")


class Sub(Foo):
    def fun(self):
        print("子类实现父类抽象方法")


su = Sub()
su.fun()
'''

# MySQL插入
'''
import MySQLdb
conn = MySQLdb.connect(host='localhost', db='search_engine',
                       user='root', passwd='root', charset='utf8')
cur = conn.cursor()
cur.execute("""insert into csdn(title,date) values(%s,%s)""", ("test", "2018-08-04 18:00:13"))
conn.commit()
'''

# 规范注释
'''
    def add(self, a: int, b: int) -> int:
        """
        :param a: int 第一个操作数
        :param b:  
        :return: 
        """
'''


"""
import requests
from lxml import etree
header = {
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}
body = requests.get("https://movie.douban.com/subject/1300267/", headers=header)
selector = etree.HTML(body.text)
fields = [s.strip().replace(':', '') for s in selector.xpath("//div[@id='info']/span[@class='pl']//text()")]
print(fields)
"""

# print(selector.xpath("//div[@id='info']//text()"))
# ['类型', '制片国家/地区', '语言', '上映日期', '片长', '又名', 'IMDb链接']

# 时间格式处理
"""
import datetime
time_str = "2018年08月04日 18:00:13"
print(datetime.datetime.strptime(time_str, "%Y年%m月%d日 %H:%M:%S"))

one = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(one, "\n", type(one))
"""

# 正则匹配
'''
import re
li = ['片长', '又名', 'IMDb链接']
test = """        
        片长: 238分钟 / 234分钟
        又名: 飘
        IMDb链接: tt0031381"""
"""
    (?:) 表示匹配括号内的正则表达式，但是这些正则表达式不能作为提取字符串使用
    例如我的re为： (?:one):\d*，匹配字符串 "one:11 one:22"的结果为 11 22,
    如果是(one):\d* 匹配字符串 "one:11 one:22"  结果是 ['one', '11', 'one', '22']
"""
values = [re.sub('\s+', ' ', s.strip()) for s in re.split('\s*(?:片长|又名|IMDb链接):\s*', test)][1:]
# ('\s*(?:%s):\s*' % '|'.join(fields), info)
print(values)

a = "1232: test,487"
print(re.sub(":.*", "", a))

s = """one:1212
    one:11111
    two:22222"""
print(re.split("(one|two):\s*", s))
'''

import redis, pickle
redis_cli = redis.StrictRedis()
# redis_cli.decr("movie_count")
print(redis_cli.get("movie_count"))

"""
def real_time_count(key, init):
    if redis_cli.get(key):
        count = pickle.loads(redis_cli.get(key))
        count = count + 1
        count = pickle.dumps(count)
        redis_cli.set(key, count)
    else:
        count = pickle.dumps(init)
        redis_cli.set(key, count)
"""


