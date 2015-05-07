# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PermissionItem(scrapy.Item):
    permission=scrapy.Field()
    desc=scrapy.Field()

class ApkItem(scrapy.Item):
    name=scrapy.Field()
    url=scrapy.Field()
    version=scrapy.Field()
    path=scrapy.Field()
    downloaded=scrapy.Field()
