# -*- coding: utf-8 -*-
import scrapy
import json
from ..sites.csdn.csdn_item import CsdnItem, CsdnItemLoader
from scrapy import Request


class CsdnSpider(scrapy.Spider):
    name = 'CSDN'
    allowed_domains = ['blog.csdn.net']
    offset = 5
    start_urls = ['https://blog.csdn.net/api/articles?type=more&category=cloud&shown_offset={}'.format(offset)]

    def parse(self, response):
        data = json.loads(response.body.decode('utf8'))

        for info in data["articles"]:
            test = dict(
                blog_id=info.get("id"),
                title=info.get("title"),
                nick_name=info.get("nickname"),
                user_url=info.get("user_url"),
                blog_url=info.get("url")
            )

            yield Request(test['blog_url'], callback=self.parse_content, meta=test)

        for i in range(self.offset, 10):
            yield Request(self.start_urls[0].format(i), callback=self.parse)

    @staticmethod
    def parse_content(response):
        data = response.meta
        item_loader = CsdnItemLoader(item=CsdnItem(), response=response)
        item_loader.add_value("blog_id", data["blog_id"])
        item_loader.add_value("title", data["title"])
        item_loader.add_xpath("content", "//div[@id='content_views']//text()")
        item_loader.add_value("nick_name", data["nick_name"])
        item_loader.add_value("user_url", data["user_url"])
        item_loader.add_value("blog_url", data["blog_url"])
        item_loader.add_xpath("date", "//span[@class='time']/text()")

        # time = response.xpath("//span[@class='time']/text()").extract_first()
        # 通过 //text()获取的是分段字符串列表
        # content = response.xpath("//div[@id='content_views']").xpath("string(.)").extract()
        # content = response.xpath("//div[@id='content_views']//text()").extract()
        # print(content)

        # 调用load_item()方法将值填充到item中？
        yield item_loader.load_item()




