# -*- coding: utf-8 -*-

import os
import configparser
# from scrapy import log
from scrapy.http import Request, Response
from scrapy import signals

import tweepy


class Twitter:
    def __init__(self, *args, **kwargs):
        super(Twitter, self).__init__(*args, **kwargs)
        self.config_file = str(os.path.dirname(os.path.abspath(__file__)) + "/config.ini")
        if os.path.exists(self.config_file):
            self.config = configparser.ConfigParser()
            self.config.read(self.config_file, "utf-8")


class TwitterUserTimelineRequest(Request):
    def __init__(self, *args, **kwargs):
        auth = kwargs.pop("auth", None)
        spider = kwargs.pop("spider", None)
        self.oauth = tweepy.OAuthHandler(auth["CONSUMER_KEY"], auth["CONSUMER_SECRET"])
        self.oauth.set_access_token(auth["ACCESS_TOKEN"], auth["ACCESS_TOKEN_SECRET"])
        super(TwitterUserTimelineRequest, self).__init__('https://twitter.com', dont_filter=True, **kwargs)


class TwitterUserTimelineResponse(Response):
    def __init__(self, *args, **kwargs):
        auth = kwargs.pop("auth", None)
        self.api = tweepy.API(auth,wait_on_rate_limit=True)
        super(TwitterUserTimelineResponse, self).__init__('https://twitter.com', *args, **kwargs)
