# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

import json

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem


class AlibbJsonPipeline(object):

    def __init__(self):
        self.file = open('items.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False).encode('utf8') + "\n"
        self.file.write(line)

        return item


class AlibbImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(request.url).hexdigest()  # change to request.url after deprecation
        goods_path=request.meta['url_hash'][0]
        shop=info.spider.name

        if request.meta['is_profile']=="true":
            return '%s/full/%s/%s/%s.jpg' % (shop,str(goods_path),"profile",image_guid)
        else:
            return '%s/full/%s/%s.jpg' % (shop,str(goods_path),image_guid)

    def get_media_requests(self, item, info):
        for profile_image_url in item['profile_img']:
            item['is_profile']="true"
            yield scrapy.Request(profile_image_url,meta=item)

        for image_url in item['image_urls']:
            item['is_profile']="false"
            yield scrapy.Request(image_url,meta=item)

    def item_completed(self, results, item, info):

        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item