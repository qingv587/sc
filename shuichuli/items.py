# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShuichuliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    vote = scrapy.Field()
    answer_list = scrapy.Field()
    catid = scrapy.Field()
    key = scrapy.Field()