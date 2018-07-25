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

    def __init__(self):
        if os.path.isfile(self.file_name):
            os.remove(self.file_name)
            print('removed products list')

    def process_item(self, item, spider):
        try:
            main_category = item['main'].strip().lower() if item['main'] is not None else None
            main_category_link = item['main_link'] if item['main_link'] is not None else None

            ProductCategoriesPipeline.save_category({
                'title': main_category,
                'link': main_category_link
            }, spider)

            for category in item['categories'] if len(item['categories']) > 0 else []:
                title = category['Category'].strip().lower() if category['Category'] is not None else None
                link = category['Category Link'] if category['Category Link'] is not None else None

                ProductCategoriesPipeline.save_category({
                    'category': {'title': title, 'link': link},
                    'parent_category': {'title': main_category, 'link': main_category_link}
                }, spider)

                for idx, v in enumerate(category['Sub Categories']):
                    ProductCategoriesPipeline.save_category({
                        'category': {'title': v.strip().lower(), 'link': category['Sub Category Links'][idx]},
                        'parent_category': {'title': title, 'link': link}
                    }, spider)

            return item
        finally:
            return item

    @staticmethod
    def save_category(category, spider):
        url = '{base_url}/categories'.format(base_url=os.getenv("SCRAPY_API_URL"))
        req = requests(url, json=category)

        if req.status_code == requests.codes.ok:
            spider.log('[API_REQUEST] successfully saved product category', logging.DEBUG)
            product_category = req.json()
            spider.log(
                '[API_REQUEST] response return {key}: {value}'.format(key='product category ID',
                                                                      value=product_category['id']),
                logging.INFO
            )
        elif req.status_code == 406:
            spider.log('[API_REQUEST] data provided was not accepted by the api', logging.ERROR)
        elif req.status_code == 500:
            spider.log('[API_REQUEST] request performed could not be finished hence', logging.ERROR)


class ProductsPipeline(object):
    url = '{base_url}/products'.format(base_url=os.getenv("SCRAPY_API_URL"))

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
                    spider.log('[API_REQUEST] category used in request does not exist', logging.WARN)
                elif req.status_code == 500:
                    spider.log('[API_REQUEST] request performed could not be finished hence', logging.ERROR)

                return item
            finally:
                return item
