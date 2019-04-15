# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
# 随机假的UserAgent
from fake_useragent import UserAgent
from .tools.get_proxy import GetIP
import browsercookie
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
"""
    ArticlespiderSpiderMiddleware和ArticlespiderDownloaderMiddleware是创建项目时自动创建的middleware
"""


class ArticlespiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ArticlespiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 随机设置爬虫的UserAgent，IP
class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # 每个交给下载器的request对象都会经过该方法，并返回期望response
    def process_request(self, request, spider):
        get_ip = GetIP()
        print("开始设置UA", "------"*30)
        request.headers.setdefault('User-Agent', self.ua.random)
        request.meta["proxy"] = get_ip.get_random_ip()


# CookiesMiddleware能自动处理Cookie，但是它不能使用浏览器的Cookie，
# 这里利用browsercookie对CookiesMiddleware进行改良，实现一个能使用浏览器Cookie的中间件
class BrowserCookiesMiddleware(CookiesMiddleware):
    """
    在构造BrowserCookiesMiddleware对象时，使用browsercookie将浏览器中的Cookie提取，存储到CookieJar字典self.jars中
    """
    def __init__(self, debug=False):
        # 这里使用super()调用基类的构造函数，然后使用load_browser_cookies()方法来加载浏览器Cookie
        super().__init__(debug)
        self.load_browser_cookies()

    def load_browser_cookies(self):
        """
        使用self.jars['chrome']和self.jars['firefox']从默认字典中获得两个CookieJar对象，
        然后调用browsercookie的chrome和firefox方法，分别获取两个浏览器中的Cookie，将它们填入各自的CookieJar对象中。
        """
        # 加载Chrome 浏览器中的Cookie
        jar = self.jars['chrome']
        chrome_cookiejar = browsercookie.chrome()
        for cookie in chrome_cookiejar:
            jar.set_cookie(cookie)

        # 加载Firefox 浏览器中的cookie
        jar = self.jars['firefox']
        firefox_cookiejar = browsercookie.firefox()
        for cookie in firefox_cookiejar:
            jar.set_cookie(cookie)
