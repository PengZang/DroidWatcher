__author__ = 'suemi'
import scrapy
from android.items  import PermissionItem
class PermissionSpider(scrapy.spider.Spider):
    name="permission"
    start_urls=["http://developer.android.com/reference/android/Manifest.permission.html"]
    def parse(self,response):
        for sel in response.xpath('//tr[re:test(@class,"api apilevel")]'):
            item=PermissionItem()
            item['permission']=sel.xpath('td[@class="jd-linkcol"]/a/text()').extract()[0]
            item['desc']=sel.xpath('td[@class="jd-descrcol"]/text()').extract()
            yield item
