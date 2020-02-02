# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PetFinderItem(scrapy.Item):
    breeds = scrapy.Field()
    url = scrapy.Field()
    attributes = scrapy.Field()
    sections = scrapy.Field()
    data = scrapy.Field()
