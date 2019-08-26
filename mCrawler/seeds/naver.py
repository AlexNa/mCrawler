import scrapy
import urllib.request
import urllib.parse
from scrapy.http import HtmlResponse
import math


class naver:
    search_url = "https://search.naver.com/search.naver"

    def __init__(self, *args, **kwargs):
        self.where = kwargs.pop('where', None)
        self.spider = kwargs.pop('spider', None)

    def get_target_urls(self):
        if self.spider:
            for keyword in self.spider.search_keywords:
                for pno in range(math.ceil(int(self.spider.count) / 10)):
                    params = {'where': self.where, 'query': 'a', 'start': (pno - 1) * 10}
                    query_string = urllib.parse.urlencode(params)
                    url = self.search_url + "?" + query_string
                    resource = urllib.request.urlopen(url)
                    content = resource.read().decode(resource.headers.get_content_charset())
                    response = HtmlResponse(url, body=content, encoding=resource.headers.get_content_charset())

                    if self.where == 'news':
                        for url in self.get_news_urls(response):
                            yield url

    def get_news_urls(self, response):
        return response.css('a._sp_each_title::attr(href)').getall()
