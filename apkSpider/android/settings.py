# -*- coding: utf-8 -*-

# Scrapy settings for android project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'android'

SPIDER_MODULES = ['android.spiders']
NEWSPIDER_MODULE = 'android.spiders'
DEFAULT_ITEM_CLASS = 'android.items.ApkItem'


ITEM_PIPELINES = {'android.pipelines.myPipeline': 1}