# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import logging
import os
import os.path
import requests
from scrapy.exceptions import DropItem

from dotenv import load_dotenv

load_dotenv()


class ProductCategoriesPipeline(object):
    file_name = 'dumps/jumia/product_categories.json'
    category_list = []
    url = '{base_url}/categories/'.format(base_url=os.getenv("SCRAPY_API_URL"))

    def process_item(self, item, spider):
        try:
            title = item['title'].strip().lower() if item['title'] is not None else None
            link = item['link'] if item['link'] is not None else None
            parent_category = item['parent'] if item['parent'] is not None else None

            if title is not None and link is not None:
                category = { 'category': { 'title': title, 'link': link }, 'parent_category': parent_category }
                requests.post(self.url, json=category)

            return item
        finally:
            return item


class ProductsPipeline(object):
    url = '{base_url}/products/'.format(base_url=os.getenv("SCRAPY_API_URL"))

    def __init__(self):
        self.skus_seen = set()

    def process_item(self, item, spider):

        if item.get('sku') is None:
            return item

        if item['sku'] in self.skus_seen:
            raise DropItem("Duplicate item found: %s" % item)

        else:
            self.skus_seen.add(item['sku'])

            try:
                # perform request to jumiabot api
                req = requests.post(self.url, json={
                    'category': item['category'],
                    'sku': item['sku'],
                    'brand': item['brand'],
                    'title': item['title'],
                    'currency': item['currency'],
                    'price': item['price'],
                    'image_url': item['image_url']
                })

                if req.status_code == requests.codes.ok:
                    spider.log('[API_REQUEST] successfully saved product', logging.DEBUG)
                    product = req.json()
                    spider.log(
                        '[API_REQUEST] response return {key}: {value}'.format(key='product ID', value=product['id']),
                        logging.INFO
                    )
                elif req.status_code == 404:
                    spider.log(req.json(), logging.WARN)
                elif req.status_code == 500:
                    spider.log(req.json(), logging.ERROR)

                return item
            finally:
                return item
