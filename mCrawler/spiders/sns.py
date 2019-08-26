# -*- coding: utf-8 -*-

# scrapy crawl sns -a search=search_data.txt -a count=100

import os
import csv
import scrapy
import datetime
from scrapy import signals
# from scrapy import log
from mCrawler.items import TwitterItem
from mCrawler.sns.twitter import Twitter, TwitterUserTimelineRequest, TwitterUserTimelineResponse
from mCrawler.common.Function import Function


class SnsSpider(scrapy.Spider):
    fields_to_export = ['uuid', 'date', 'sns_from', 'content_id', 'post_date', 'user_id', 'user_name',
                        'content']

    name = 'sns'
    custom_settings = {
        'ITEM_PIPELINES': {'mCrawler.pipelines.CSVWriterPipeline': 400},
        'DOWNLOADER_MIDDLEWARES': {'mCrawler.spiders.sns.snsDownloaderMiddleware': 400},
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
        super(SnsSpider, self).__init__(*args, **kwargs)
        self.count = count
        self.search = search
        self.Twitter = Twitter()

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
        if self.Twitter.config:
            for acc in self.Twitter.config.keys():
                if acc.find('TWITTER') > -1:
                    yield TwitterUserTimelineRequest(self.parse, spider=self, auth=self.Twitter.config[acc])

    def parse(self, response):
        if isinstance(response, TwitterUserTimelineResponse):
            try:

               for keyword in self.search_keywords:
                    public_tweets = response.api.search(q=keyword, count=self.count)
                    for tweet in public_tweets:
                        item = TwitterItem()
                        item["sns_from"] = 'twitter'
                        item["content_id"] = tweet.id_str
                        item["user_id"] = tweet.user.id_str
                        item["user_name"] = tweet.user.name
                        item["post_date"] = tweet.created_at.strftime("%Y%m%d%H%M%S")
                        item["content"] = Function.remove_carriage_return(tweet.text)
                        yield item
            except Exception as err:
                pass
                # raise scrapy.exceptions.CloseSpider("Twitter Authentication Fail %s" % str(err))
                # log.msg('---------------------------->Twitter Authentication Fail %s' % str(err), level=log.INFO)


class snsDownloaderMiddleware(object):
    def __init__(self, *args, **kwargs):
        super(snsDownloaderMiddleware, self).__init__(*args, **kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if isinstance(request, TwitterUserTimelineRequest):
            return TwitterUserTimelineResponse(auth=request.oauth)

        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Sns opened: %s' % spider.name)
