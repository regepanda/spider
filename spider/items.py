# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiajiaItem(scrapy.Item):
    # define the fields for your item here like:
    imgs = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    onePrice = scrapy.Field()
    room = scrapy.Field()
    communityName = scrapy.Field()
    area = scrapy.Field()
