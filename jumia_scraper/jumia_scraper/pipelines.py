# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import json
import os
import os.path

from scrapy.exceptions import DropItem


class ProductCategoriesPipeline(object):
    file_name = 'dumps/jumia/product_categories.json'
    category_list = []

    def __init__(self):
        if os.path.isfile(self.file_name):
            os.remove(self.file_name)
            print('removed products list')

    def process_item(self, item, spider):
        try:
            # print(dir(spider))
            main_category = item['main'] if item['main'] is not None else None
            main_category_link = item['main_link'] if item['main_link'] is not None else None
            categories = item['categories'] if len(item['categories']) > 0 else []

            for category in categories:
                title = category['Category'] if category['Category'] is not None else None
                link = category['Category Link'] if category['Category Link'] is not None else None
                sub_categories = [{'title': v.strip().lower(), 'link': category['Sub Category Links'][idx]} for idx, v
                                  in enumerate(category['Sub Categories'])]
                parent_category = {'link': main_category_link,
                                   'title': main_category.strip().lower()} if main_category is not None else None

                self.category_list.append({
                    'title': title,
                    'link': link,
                    'sub_categories': sub_categories,
                    'parent': parent_category
                })

            with open(self.file_name, 'w') as outfile:
                json.dump(self.category_list, outfile, indent=4, skipkeys=True)

            return item
        finally:
            return item


class ProductsPipeline(object):

    def __init__(self):
        self.skus_seen = set()

        if not os.path.isfile('dumps/jumia/jumia_products.csv'):
            self.csvwriter = csv.writer(open('dumps/jumia/jumia_products.csv', 'a'))
            self.csvwriter.writerow(
                ['category', 'product_sku', 'brand', 'title', 'currency', 'price', 'product_image_url'])
        else:
            self.csvwriter = csv.writer(open('dumps/jumia/jumia_products.csv', 'a'))

    def process_item(self, item, spider):

        if item.get('sku') is None:
            return item

        if item['sku'] in self.skus_seen:
            raise DropItem("Duplicate item found: %s" % item)

        else:
            self.skus_seen.add(item['sku'])
            # return item  
            self.csvwriter.writerow([
                item['category'],
                item['sku'],
                item['brand'],
                item['title'],
                item['currency'],
                item['price'],
                item['image_url']
            ])
            return item
