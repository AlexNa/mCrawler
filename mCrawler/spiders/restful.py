import os
import scrapy
import datetime
import json
import urllib.parse
from mCrawler.items import RestfulItem

# scrapy crawl restful -a url=https://httpbin.org/get -a method=GET

class RestfulSpider(scrapy.Spider):
    name = 'restful'

    search_apis = []

    custom_settings = {
        'ITEM_PIPELINES':
            {'mCrawler.pipelines.PlainWriterPipeline': 400},
        'LOG_ENABLED': 'True',
        'LOG_LEVEL': 'INFO',
    }

    def __init__(self, search=None, output=None, *args, **kwargs):
        if not output:
            self.output_filename = datetime.datetime.now().strftime("%Y%m%d%H%M") + ".dat"
        else:
            self.output_filename = output
        super(RestfulSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        if hasattr(self, 'url') and hasattr(self, 'method'):
            if self.method.upper() == 'GET':
                yield scrapy.Request(self.url, callback=self.parse, method="GET")
            if self.method.upper() == 'POST':
                yield scrapy.FormRequest(self.url, callback=self.parse)

    def parse(self, response):
        item = json.loads(response.text)
        yield item
