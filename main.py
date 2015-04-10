# !/usr/bin/env python
#-*- coding: utf-8 -*-
#__author__ = 'Ario'


from scrapy.cmdline import execute

if __name__=='main':
    execute("scrapy crawl dmoz".split())