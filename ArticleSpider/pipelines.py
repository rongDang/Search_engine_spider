# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi

from .models.es_types import DouBan
from elasticsearch_dsl.connections import connections

es_douban = connections.create_connection(DouBan)


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLAsyncPipeline(object):

    # spider开始时
    def open_spider(self, spider):
        # spider.settings.get 从settings配置文件获取参数信息
        params = dict(
            db=spider.settings.get("MYSQL_DB_NAME"),
            host=spider.settings.get("MYSQL_HOST"),
            port=spider.settings.get("MYSQL_PORT"),
            user=spider.settings.get("MYSQL_USER"),
            passwd=spider.settings.get("MYSQL_PASSWORD"),
            charset="utf8mb4",
        )

        # 创建一个连接池
        self.dbpool = adbapi.ConnectionPool("MySQLdb", **params)

    # spider关闭时，关闭连接池
    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        # 以异步的方式调用insert_db函数，item会被传给insert_db的第二个参数，
        # insert_db第一个参数是一个Transaction对象，和Cursor类似
        self.dbpool.runInteraction(self.insert_mysql, item)
        return item

    @staticmethod
    def insert_mysql(tx, item):
        print("进入到执行MySQL的  insert_mysql 中")
        # 从item中获取对应的sql语句和values值
        sql, values = item.save_to_mysql()
        # 执行sql后，会自动调用commit方法
        tx.execute(sql, values)


class ElasticSearchPipeline(object):

    def process_item(self, item, spider):
        item.save_to_es()
        return item



