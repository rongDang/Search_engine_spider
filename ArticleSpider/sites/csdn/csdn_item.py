# -*- encoding:utf8 -*-
import scrapy
import redis
import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity
from ArticleSpider.items import MysqlItem, ElasticSearchItem
from ArticleSpider.sites.csdn.es_csdn import CsdnBlogIndex
from ArticleSpider.tools.es_suggests import generate_suggests

# 与Elasticsearch进行连接，
from elasticsearch_dsl import connections
es_csdn = connections.create_connection(CsdnBlogIndex)
# 创建和redis的连接
redis_cli = redis.StrictRedis()


class CsdnItemLoader(ItemLoader):
    """
        自定义item loader ，默认输出第一个值, 这样在spider中就不需要使用extract_first()
    """
    default_output_processor = TakeFirst()


class CsdnItem(scrapy.Item, MysqlItem, ElasticSearchItem):
    """
        :param 博客id，标题，内容，用户昵称，用户地址，博客地址，时间
    """

    table_name = "csdn"

    blog_id = scrapy.Field()
    title = scrapy.Field()
    # 这里设置输出处理为默认的Identity()，返回原理的值
    content = scrapy.Field(output_processor=Identity())
    nick_name = scrapy.Field()
    user_url = scrapy.Field()
    blog_url = scrapy.Field()
    date = scrapy.Field()

    def clean_data(self):
        """
            需要对文章的内容，日期进行处理
        """
        text = ""
        for i in self["content"]:
            j = i.replace("\t", "")
            text += j.replace("\n", "")
        self["content"] = text

        # 对日期进行处理, 这里需要注意，在第一个pipeline中如果调用了clean_date函数，那么content和date已经被处理，
        # 后面的pipeline接受到的item中的 content和date都已经被处理过了，理论后面的pipeline无需调用clean_data好函数
        # 但是得注意settings中pipeline对应值的顺序
        print("处理前的date: ", self["date"])
        try:
            blog_time = datetime.datetime.strptime(self["date"], "%Y年%m月%d日 %H:%M:%S")
            self["date"] = blog_time.strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass
        print("处理后的date: ", self["date"])

    def save_to_mysql(self):
        self.clean_data()

        insert_sql = """insert into csdn(blog_id, title, content, nick_name, user_url, blog_url, date)
         values(%s, %s, %s, %s, %s, %s, %s)"""

        insert_params = (
            self["blog_id"],
            self['title'],
            self['content'],
            self['nick_name'],
            self['user_url'],
            self['blog_url'],
            self['date']
        )
        print(insert_params)
        return insert_sql, insert_params

    def save_to_es(self):
        self.clean_data()
        print("save_to_es:", self["date"], "------"*30)
        csdn = CsdnBlogIndex()
        csdn.blog_id = self["blog_id"]
        csdn.title = self["title"]
        csdn.content = self["content"]
        csdn.nick_name = self["nick_name"]
        csdn.user_url = self["user_url"]
        csdn.blog_url = self["blog_url"]
        csdn.date = self["date"]

        # 生成搜索建议(suggest)存到es中, 传入要生成suggest的字段，和对应字段的权重
        csdn.suggest = generate_suggests(es_csdn, ((csdn.title, 5),
                                                   (csdn.content, 2),
                                                   (csdn.nick_name, 1))
                                         )

        redis_cli.incr("csdn_count")
        # 保存数据
        csdn.save()



