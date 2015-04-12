# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class AlibbItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    url_hash=Field()
    name = Field()
    boothes = Field()
    is_profile = Field()
    price=Field()
    attributes=Field()
    properties=Field()
    detail_data=Field()
    parameters=Field()

    #img
    photos=Field()
    image_paths=Field()
    images =Field()