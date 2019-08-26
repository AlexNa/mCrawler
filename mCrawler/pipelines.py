# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from __future__ import unicode_literals
from scrapy.exporters import JsonItemExporter, CsvItemExporter, XmlItemExporter, PythonItemExporter
import sys
import os
from scrapy.exceptions import DropItem
import json
import csv
import uuid
import datetime
from mCrawler.items import NewsItem


class PlainWriterPipeline(object):
    def open_spider(self, spider):
        file = open(spider.output_filename, 'wb')
        self.file_handle = file

    def close_spider(self, spider):
        self.file_handle.close()

        full_path = os.getcwd() + os.sep + spider.output_filename
        sys.stdout.write(full_path)
        sys.stdout.flush()

    def process_item(self, item, spider):
        self.file_handle.write(str(item).encode('utf-8'))
        return item

class JsonWriterPipeline(object):
    def open_spider(self, spider):
        file = open(spider.output_filename, 'wb')
        self.file_handle = file
        self.exporter = JsonItemExporter(file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file_handle.close()

        full_path = os.getcwd() + os.sep + spider.output_filename
        sys.stdout.write(full_path)
        sys.stdout.flush()
        # sys.stderr.write(full_path)
        # sys.stderr.flush()

    def process_item(self, item, spider):
        item.setdefault('uuid', str(uuid.uuid1()))
        item.setdefault('date', datetime.datetime.now().strftime("%Y%m%d%H%M"))
        self.exporter.fields_to_export = spider.fields_to_export
        for field in item.keys():
            if field not in self.exporter.fields_to_export:
                self.exporter.fields_to_export.append(field)

        self.exporter.export_item(item)
        return item


class CSVWriterPipeline(object):

    def open_spider(self, spider):
        file = open(spider.output_filename, 'wb')
        self.file_handle = file
        self.exporter = CsvItemExporter(file, delimiter='\t')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file_handle.close()
        full_path = os.getcwd() + os.sep + spider.output_filename
        sys.stdout.write(full_path)
        sys.stdout.flush()
        # sys.stderr.write(full_path)
        # sys.stderr.flush()

    def process_item(self, item, spider):
        item.setdefault('uuid', str(uuid.uuid1()))
        item.setdefault('date', datetime.datetime.now().strftime("%Y%m%d%H%M"))
        self.exporter.fields_to_export = spider.fields_to_export
        for field in item.keys():
            if field not in self.exporter.fields_to_export:
                self.exporter.fields_to_export.append(field)
        self.exporter.export_item(item)
        return item
