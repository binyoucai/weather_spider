# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
import redis
from scrapy.exceptions import DropItem


class RedisPipeline(object):
    '''
    redis存储，过滤器
    '''

    def __init__(self, db_config):
        self.db_config = db_config

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_config=crawler.settings.get('DATABASES_CONFIG').get('redis')
        )

    def open_spider(self, spider):
        self.r = redis.Redis(**self.db_config)

    def process_item(self, item, spider):
        if self.r.sadd(spider.name+':items', item['city']+item['ymd']):
            return item
        raise DropItem

class MongodbPipeline(object):
    '''
    mongodb存储
    '''

    def __init__(self, db_config):
        self.mongo_uri = db_config.get('uri')
        self.mongo_db = db_config.get('db')
        print(self.mongo_uri)
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_config=crawler.settings.get('DATABASES_CONFIG').get('mongodb')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.table_name
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline(object):
    '''
    mysql存储，增量式更新
    '''

    def __init__(self, db_config):
        self.db_config = db_config

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_config=crawler.settings.get('DATABASES_CONFIG').get('mysql')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(**self.db_config)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        keys, values = zip(*item.items())
        table_name = item.table_name
        sql = "insert into `{}` ({}) values ({}) " \
              "ON DUPLICATE KEY UPDATE {}".format(
            table_name,
            ','.join(keys),
            ','.join(['%s'] * len(values)),
            ','.join(['`{}`=%s'.format(k) for k in keys])
        )
        self.cur.execute(sql, values * 2)
        self.conn.commit()
        return item
