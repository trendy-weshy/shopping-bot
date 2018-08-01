# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductCategories(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    parent = scrapy.Field()


class Products(scrapy.Item):
    category = scrapy.Field()
    brand = scrapy.Field()
    title = scrapy.Field()
    sku = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    image_url = scrapy.Field()
    image = scrapy.Field()