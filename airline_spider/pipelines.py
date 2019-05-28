# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo
import logging


class SpiderCorePipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        user_name = settings['USER_NAME']
        password = settings['PASSWORD']
        client = pymongo.MongoClient(host=host, port=port, username=user_name, password=password)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        #logging.info("item:{}".format(item))
        try:
            air_item = dict(item)
            # logging.info("保存数据:air_item".format(air_item))
            if air_item.get('air_No') is not None:
                print(air_item)
                self.post.insert(air_item)
        except Exception as e:
            logging.error("保存错误!,e:{}".format(e))
        return item
