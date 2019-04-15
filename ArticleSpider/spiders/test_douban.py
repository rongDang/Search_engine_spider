# -*- coding: utf-8 -*-
import scrapy, json, re
from scrapy import Request


class DoubanSpider(scrapy.Spider):
    name = 'test_douban'
    BASE_URL = "https://movie.douban.com/j/search_subjects?type=movie&tag={}&sort=recommend&page_limit={}&page_start={}"
    MOVIE_TAG = '豆瓣高分'
    PAGE_LIMIT = 20
    page_start = 0
    start_urls = [BASE_URL.format(MOVIE_TAG, PAGE_LIMIT, page_start)]

    def parse(self, response):
        # 将json字符串转化为json格式
        infos = json.loads(response.body.decode('utf8'))

        for movie_info in infos['subjects']:
            movie_item = {}
            movie_item['片名'] = movie_info['title']
            movie_item['评分'] = movie_info['rate']
            # 再次请求解析的url，调用回调函数，同时将解析出来的数据通过meta传过去
            yield Request(movie_info['url'], callback=self.parse_movie, meta={'_movie_item': movie_item})

        # 如果json 结果中包含的影片数量小于请求数量，说明没有影片了，否则继续搜索
        if len(infos['subjects']) == self.PAGE_LIMIT:
            self.page_start += self.PAGE_LIMIT
            url = self.BASE_URL.format(self.MOVIE_TAG, self.PAGE_LIMIT, self.page_start)
            yield Request(url)

    @staticmethod
    def parse_movie(response):
        movie_item = response.meta['_movie_item']
        info = response.css('div.subject div#info').xpath('string(.)').extract_first()
        fields = [s.strip().replace(':', '') for s in response.css('div#info span.pl::text').extract()]
        values = [re.sub('\s+', ' ', s.strip()) for s in re.split('\s*(?:%s):\s*' % '|'.join(fields), info)][1:]
        movie_item.update(dict(zip(fields, values)))
        print(movie_item)
        yield movie_item


"""测试代理IP，
def start_requests(self):
    for _ in range(10):
        yield Request('http://httpbin.org/ip', dont_filter=True)
        yield Request('https://httpbin.org/ip', dont_filter=True)

def parse(self, response):
    print(json.loads(response.text))
"""