# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
from ArticleSpider.sites.douban.douban_item import DouBanItem, DouBanItemLoader
import re


class DoubanSpider(scrapy.Spider):
    """
    movie_id*, name*, alias, introduce, url*, directors*, rate*, casts*, type, date
    """
    name = 'douban'
    base_url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags={}&start={}'
    tag = "短片"
    start = 0
    start_urls = [base_url.format(tag, start)]
    # start_urls = ["https://movie.douban.com/subject/1292052/"]'https://movie.douban.com/subject/1469165/'

    def parse(self, response):
        data = json.loads(response.body.decode('utf8'))
        for info in data["data"]:
            # 可能会出现没有对应键，使用 get 方式更保险
            message = dict(
                movie_id=info.get("id"),
                name=info.get("title"),
                url=info.get("url"),
                directors=info.get("directors", ["未知"]),
                rate=info.get("rate", 0),
                casts=info.get("casts", ["未知"])
            )
            yield Request(message["url"], callback=self.parse_content, meta=message)

        for num in range(self.start, 600, 20):
            url = self.base_url.format(self.tag, num)
            print("正在从第{}条数据开始爬取：".format(num))
            yield Request(url, callback=self.parse)

    @staticmethod
    def parse_content(response):
        data = response.meta

        # 获取电影的所有基本信息
        all_text = response.xpath("//div[@id='info']").xpath('string(.)').extract_first()
        # 取处类似 '语言:' 这样的键
        fields = [s.strip().replace(':', '') for s in response.css('div#info span.pl::text').extract()]
        # 通过正则匹配，匹配键后面的值
        values = [re.sub('\s+', ' ', s.strip()) for s in re.split('\s*(?:%s):\s*' % '|'.join(fields), all_text)][1:]
        di = dict(zip(fields, values))

        introduce = " "
        for i in response.xpath("//div[@class='indent']/span[1]//text()").extract():
            j = i.replace("\t", "")
            introduce += j.replace("\n", "")

        item_loader = DouBanItemLoader(item=DouBanItem(), response=response)
        item_loader.add_value("movie_id", data["movie_id"])
        item_loader.add_value("name", data["name"])
        item_loader.add_value("url", data["url"])
        item_loader.add_value("directors", "/ ".join(data["directors"]))
        item_loader.add_value("rate", data["rate"])
        item_loader.add_value("casts", "/ ".join(data["casts"]))
        item_loader.add_value("introduce", introduce)
        if di.get("又名"):
            item_loader.add_value("alias", di.get("又名"))
        else:
            item_loader.add_value("alias", "暂无别名")

        if di.get("类型"):
            item_loader.add_value("type", di.get("类型"))
        else:
            item_loader.add_value("type", "无")

        if di.get("上映日期"):
            item_loader.add_value("date",  di.get("上映日期"))
        else:
            item_loader.add_value("date", "未知年份")

        yield item_loader.load_item()
