# -*- coding: utf-8 -*-

# scrapy crawl web -a search=search_urls.txt

import os
import csv
import scrapy
import datetime
from scrapy import signals
# from scrapy import log
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import fnmatch
import re
from urllib.parse import urlparse
from mCrawler.items import WebItem
from bs4 import BeautifulSoup
from mCrawler.common.Function import Function
import tldextract


class WebSpider(scrapy.Spider):
    fields_to_export = ['uuid', 'date', 'domain', 'url', 'content']

    name = 'web'

    custom_settings = {
        'ITEM_PIPELINES':
            {'mCrawler.pipelines.CSVWriterPipeline': 400},
        'LOG_ENABLED': 'True',
        'LOG_LEVEL': 'INFO',
    }

    requests_urls = []

    def __init__(self, search=None, output=None, count=100, *args, **kwargs):
        if not search:
            raise scrapy.exceptions.CloseSpider("Required Argument 'search'")
        if not output:
            self.output_filename = datetime.datetime.now().strftime("%Y%m%d%H%M") + ".dat"
        else:
            self.output_filename = output
        super(WebSpider, self).__init__(*args, **kwargs)
        self.search = search
        if hasattr(self, 'search'):
            if os.path.exists(self.search):
                with open(self.search, newline='', encoding="utf-8") as csvfile:
                    csvreader = csv.reader(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for row in csvreader:
                        if row and len(row) > 0:
                            self.start_urls.append(row[0].strip())
            else:
                raise scrapy.exceptions.CloseSpider("'search' file is not exits")

    def start_requests(self):
        for url in self.start_urls:
            if url not in self.requests_urls:
                self.requests_urls.append(url)
                yield scrapy.Request(url, self.parse)

    def parse(self, response):
        ext = tldextract.extract(urlparse(response.url).netloc)
        domain = ext.registered_domain
        ext = DomainPatternLinkExtractor(domain, canonicalize=True, unique=True)
        urls = []
        try:
            if response.headers['Content-Type'] \
                    and response.headers['Content-Type'].decode("utf-8").lower().find("application") == -1:
                urls = [link.url for link in ext.extract_links(response)]
            else:
                return
        except Exception as ex:
            # log.msg('----------------------------> %s --> %s' % (response.headers['Content-Type'], ex), level=log.INFO)
            pass
        for url in urls:
            if url not in self.requests_urls:
                self.requests_urls.append(url)
                yield response.follow(url, self.parse)
        item = WebItem()
        item['url'] = response.url
        item['domain'] = domain
        try:
            item['content'] = Function.get_text(response.text)
            yield item
        except Exception as ex:
            # log.msg('----------------------------> %s --> %s' % (response.headers['Content-Type'], ex), level=log.INFO)
            pass


class DomainPatternLinkExtractor(LinkExtractor):
    def __init__(self, domain_pattern, *args, **kwargs):
        super(DomainPatternLinkExtractor, self).__init__(*args, **kwargs)
        regex = fnmatch.translate(domain_pattern)
        self.reobj = re.compile(regex)

    def extract_links(self, response):
        return list(
            filter(
                lambda link: self.reobj.search(urlparse(link.url).netloc),
                super(DomainPatternLinkExtractor, self).extract_links(response)
            )
        )
