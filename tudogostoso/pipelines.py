# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import psycopg2
from datetime import datetime

def has_all_attributes(item):
    return 'name' in item and 'image_url' in item and 'time_to_prepare' in item and 'recipe_yield' in item and 'ingredients' in item and 'instructions' in item

def format_pg_array(a):
    pg_array = "ARRAY["

    for i in range(len(a)):
        if i != len(a) - 1:
            pg_array += "'%s'," %(a[i])
        else:
            pg_array += "'%s'" %(a[i])

    pg_array += "]"
    return pg_array

class ValidateValuesPipeLine(object):
    def process_item(self, item, spider):
        if has_all_attributes(item):
          return item
        else:
          raise DropItem("Missing attribute in %s" % item)

class PostgresPipeLine(object):
    table_name = 'recipes'

    def __init__(self, db_host, db_name, db_user, db_pw):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_pw = db_pw

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_host=crawler.settings.get('DB_HOST'),
            db_name=crawler.settings.get('DB_NAME'),
            db_user=crawler.settings.get('DB_USER'),
            db_pw=crawler.settings.get('DB_PASSWORD'),
        )

    def open_spider(self, spider):
        try:
            self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %(self.db_name, self.db_user, self.db_host, self.db_pw))
        except Exception, e:
          print e

        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()


    def process_item(self, item, spider):
        self.cursor.execute("INSERT INTO recipes(name, image, time_to_prepare, yield, method_of_preparation, ingredients, created_at, updated_at) VALUES('%s', '%s', %d, %d, %s, %s, '%s', '%s')" %(item['name'], item['image_url'], item['time_to_prepare'], item['recipe_yield'], format_pg_array(item['instructions']), format_pg_array(item['ingredients']), str(datetime.now()), str(datetime.now())))
        self.conn.commit()

        return item
