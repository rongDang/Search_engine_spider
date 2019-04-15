# -*- encoding:utf8 -*-
import scrapy
import redis
import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity
from ArticleSpider.items import MysqlItem, ElasticSearchItem
from ArticleSpider.sites.douban.es_douban import DouBanIndex
from ArticleSpider.tools.es_suggests import generate_suggests

# 与Elasticsearch进行连接，
from elasticsearch_dsl import connections
es_douban = connections.create_connection(DouBanIndex)
# 创建和redis的连接
redis_cli = redis.StrictRedis()


class DouBanItemLoader(ItemLoader):
    """
        自定义item loader ，默认输出第一个值, 这样在spider中就不需要使用extract_first()
    """
    default_output_processor = TakeFirst()


class DouBanItem(scrapy.Item, MysqlItem, ElasticSearchItem):
    """
        电影id，电影名，评分，别名，简介，链接，导演，演员，类型，上映时间
    """

    table_name = "douban"

    movie_id = scrapy.Field()
    name = scrapy.Field()
    rate = scrapy.Field()
    alias = scrapy.Field()
    introduce = scrapy.Field()
    url = scrapy.Field()
    directors = scrapy.Field()
    casts = scrapy.Field()
    type = scrapy.Field()
    date = scrapy.Field()

    def clean_data(self):
        pass

    def save_to_mysql(self):
        insert_sql = """insert into douban(movie_id, name, alias, introduce, url, directors, rate, casts, type, date) 
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        insert_params = (
            self["movie_id"],
            self["name"],
            self["alias"],
            self["introduce"],
            self["url"],
            self["directors"],
            self["rate"],
            self["casts"],
            self["type"],
            self["date"]
        )
        return insert_sql, insert_params

    def save_to_es(self):
        movie = DouBanIndex()
        movie.movie_id = self["movie_id"]
        movie.name = self["name"]
        movie.alias = self["alias"]
        movie.introduce = self["introduce"]
        movie.url = self["url"]
        movie.directors = self["directors"]
        movie.rate = self["rate"]
        movie.casts = self["casts"]
        movie.type = self["type"]
        movie.date = self["date"]

        # 给对应字段生成suggest，方便查询
        movie.suggest = generate_suggests(es_douban, ((movie.name, 6),
                                                      (movie.alias, 3),
                                                      (movie.introduce, 2))
                                          )
        # 给redis中，键为movie_count的值加1
        redis_cli.incr("movie_count")
        movie.save()




