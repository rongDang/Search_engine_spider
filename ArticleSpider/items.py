# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from abc import ABCMeta, abstractmethod


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BaseItem(metaclass=ABCMeta):

    @abstractmethod
    def clean_data(self):
        """
        :return: 对提取的数据进行清洗
        """


class MysqlItem(BaseItem):
    """
        数据存储到MySQL中应该实现的接口
    """
    table_name = ""     # 数据库表名

    @abstractmethod
    def save_to_mysql(self):
        """
        :return: 返回需要执行的sql语句 和 sql中的参数
        """


class ElasticSearchItem(BaseItem):
    """
        数据存储到ElasticSearch中需要实现的接口
    """

    @abstractmethod
    def save_to_es(self):
        """
        :return: 将数据存到es上
        """

