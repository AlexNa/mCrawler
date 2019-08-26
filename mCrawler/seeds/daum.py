import os
import scrapy
import urllib.request
import urllib.parse
from scrapy.http import HtmlResponse
import math


class daum:
    search_url = "https://search.daum.net/search"

    def __init__(self, *args, **kwargs):
        self.where = kwargs.pop('where', None)
        self.spider = kwargs.pop('spider', None)

    def get_target_urls(self):
        if self.spider:
            for keyword in self.spider.search_keywords:
                for pno in range(math.ceil(int(self.spider.count) / 10)):
                    params = {'w': self.where, 'q': keyword, 'p': pno}
                    query_string = urllib.parse.urlencode(params)
                    url = self.search_url + "?" + query_string
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
                    req = urllib.request.Request(url, headers=headers)
                    resource = urllib.request.urlopen(req)
                    content = resource.read().decode(resource.headers.get_content_charset())
                    response = HtmlResponse(url, body=content, encoding=resource.headers.get_content_charset())

                    if self.where == 'news':
                        for url in self.get_news_urls(response):
                            yield url

    def get_news_urls(self, response):
        return response.css('a.f_link_b::attr(href)').getall()
