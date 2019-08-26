# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class baseItem(scrapy.Item):
    uuid = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()

class NewsItem(baseItem):
    encode = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    meta_tag = scrapy.Field()

class TwitterItem(baseItem):
    sns_from = Field()
    content_id = Field()
    content = Field()
    post_date = Field()
    user_id = Field()
    user_name = Field()

class WebItem(baseItem):
    domain = Field()
    content = Field()