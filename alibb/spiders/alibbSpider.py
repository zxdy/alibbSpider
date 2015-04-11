# !/usr/bin/env python
#-*- coding: utf-8 -*-
#__author__ = 'Ario'
import hashlib
import json
import re
import sys

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.http import  Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
# noinspection PyUnresolvedReferences
from alibb.alibbItems import AlibbItem

class alibbSpider(scrapy.Spider):
    name = "jinlp1688"
    allowed_domains = ["1688.com","taobaocdn.com"]
    start_urls = [
        "http://jinlp1688.1688.com/page/offerlist.htm"
    ]


    link_extractor = {
        'page':  SgmlLinkExtractor(allow = '/page/.*htm.*pageNum=\d.*'),
        'page_down':  SgmlLinkExtractor(allow = '/page/.*htm.*pageNum=\d.*'),
        'content_down': SgmlLinkExtractor(allow_domains = 'taobaocdn.com',allow='.*'),
        'content':  SgmlLinkExtractor(allow = '/offer/\w+\.html'),
    }

    _x_query = {
        'title':    '//*[@id="mod-detail-title"]/h1/text()',
        'detail_info':'//*[@id="mod-detail-attributes"]/div[1]/table/tbody/tr/td/text()',
        'cdn_img':'//img/@src',
        'price':'//span[re:test(@class,"value price-length-\d$")]/text()'
    }


    def parse(self, response):
        links=self.link_extractor['page'].extract_links(response)
        for link in links:
            yield Request(url = link.url, callback=self.parse_page)

    def parse_page(self, response):
        for link in self.link_extractor['page_down'].extract_links(response):
            yield Request(url = link.url, callback=self.parse_page)

        for link in self.link_extractor['content'].extract_links(response):
            yield Request(url = link.url, callback=self.parse_content)

    def parse_content_down(self,response):

        img_urls=response.xpath(self._x_query['cdn_img']).re('.*jpg.*|.*jpeg.*|.*png.*')

        goods_loader = response.meta['item']
        goods_loader.add_value('image_urls',img_urls)
        return goods_loader.load_item()

    def parse_content(self, response):

        goods_loader = ItemLoader(item=AlibbItem(), response = response)
        url = str(response.url)
        goods_loader.add_value('url', url)
        goods_loader.add_value('url_hash',hashlib.sha1(url).hexdigest())
        goods_loader.add_xpath('title', self._x_query['title'].encode('utf-8'))
        goods_loader.add_xpath('price',self._x_query['price'])


        # detail data
        iDetailDataPattern=re.compile("iDetailData.*};",re.DOTALL)
        detail_data_list=response.xpath('//script').re(iDetailDataPattern)
        detail_data=detail_data_list[0].replace("iDetailData = {","{")
        detail_data=detail_data.replace("};","}")
        detail_data=detail_data.replace("\t|\n|\\","")
        detail_data_json=json.loads(detail_data)
        goods_loader.add_value('detail_data',detail_data_json)

        # detail information
        detail_info_list=response.xpath(self._x_query['detail_info']).extract()
        goods_loader.add_value('detail_info', dict(zip(detail_info_list[::2],detail_info_list[1::2])))
        print goods_loader.load_item()['url']

        # big img
        for link in response.xpath('//*[@id="desc-lazyload-container"]/@data-tfs-url').extract():
            yield Request(url = link, meta={'item': goods_loader},callback=self.parse_content_down)

