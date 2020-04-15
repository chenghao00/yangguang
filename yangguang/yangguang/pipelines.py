# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo
import re
class YangguangPipeline(object):
    # 从配置信息中拿到mongo的信息并赋值
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    # 从settings里拿到一些配置信息
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    # mongodb初始化对象声明
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    # item插入到mongodb
    def process_item(self, item, spider):
        name = item.__class__.__name__
        item["content"] = self.process_content(item["content"])
        print(item)

        self.db[name].insert(dict(item))
        return item

    # 使mongodb链接信息关闭，释放内存
    def close_spider(self, spider):
        self.client.close()

    def process_content(self, content):
        content = re.sub(r"\u3000|\r\n", "", content)
        #content = [i for i in content if len(i) > 0]  # 去除列表中的空字符串
        return content