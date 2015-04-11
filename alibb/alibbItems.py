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
    title = Field()
    profile_img = Field()
    price=Field()

    detail_info=Field()

    #img
    image_urls=Field()
    image_paths=Field()
    images =Field()