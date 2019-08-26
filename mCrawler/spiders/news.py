# -*- coding: utf-8 -*-

# scrapy crawl news -a search=search_data.txt --nolog
# scrapy crawl news -a search=search_data.txt -a count=10

import os
import scrapy
# from scrapy import log
import datetime
import json
from urllib.parse import urlparse
from urllib import parse as en_urlparse
from mCrawler.items import NewsItem
import csv
from bs4 import BeautifulSoup

import w3lib.encoding

from mCrawler.news.news import news
from mCrawler.seeds.naver import naver
from mCrawler.seeds.daum import daum

from mCrawler.common.Function import Function


class NewsSpider(scrapy.Spider):
    fields_to_export = ['uuid', 'date', 'url', 'title', 'content']

    name = 'news'

    custom_settings = {
        'ITEM_PIPELINES':
            {'mCrawler.pipelines.CSVWriterPipeline': 400},
        'LOG_ENABLED': 'True',
        'LOG_LEVEL': 'INFO',
    }

    search_keywords = []

    def __init__(self, search=None, output=None, count=100, *args, **kwargs):
        if not search:
            raise scrapy.exceptions.CloseSpider("Required Argument 'search'")
        if not output:
            self.output_filename = datetime.datetime.now().strftime("%Y%m%d%H%M") + ".dat"
        else:
            self.output_filename = output
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.count = count
        self.search = search
        self.news = news()
        self.naver = naver(where="news", spider=self)
        self.daum = daum(where="news", spider=self)
        self.title_seletor = self.news.title_seletor
        self.content_seletor = self.news.content_seletor

    def start_requests(self):
        if hasattr(self, 'search'):
            if os.path.exists(self.search):
                with open(self.search, newline='', encoding="utf-8") as csvfile:
                    csvreader = csv.reader(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for row in csvreader:
                        if row and len(row) > 0:
                            self.search_keywords.append(row[0].strip())
            else:
                raise scrapy.exceptions.CloseSpider("'search' file is not exits")

        for url in self.naver.get_target_urls():
            yield scrapy.Request(url, self.parse)

        for url in self.daum.get_target_urls():
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        item = NewsItem()
        url = "{0.scheme}://{0.netloc}/".format(urlparse(response.url))

        item['url'] = response.url

        title = self.get_title_by_selector(response)
        content = self.get_content_by_selector(response)

        # if not title:

        if title:
            item['title'] = title

        if content:
            item['content'] = content

        if 'content' not in item.keys():
            item['content'] = "**None Selector**"

        if 'title' not in item.keys():
            item['title'] = "**None Selector**"
        yield item

    def get_title_by_selector(self, response):
        if self.title_seletor:
            for sel in self.title_seletor:
                title = ''.join(response.css(sel).extract()).strip()
                if title:
                    title = Function.get_text(title)
                    return title

    def get_content_by_selector(self, response):
        if self.content_seletor:
            for sel in self.content_seletor:
                content = ''.join(response.css(sel).extract()).strip()
                if content:
                    content = Function.get_text(content)
                    return content
