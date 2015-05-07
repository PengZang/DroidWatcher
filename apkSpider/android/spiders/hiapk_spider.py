__author__ = 'suemi'
import scrapy
from android.items import ApkItem
from scrapy.http import Request
from multiprocessing import Pool
import urllib,os

class HiapkSpider(scrapy.spider.Spider):
    name="hiapk"
    allowed_domains=['apk.hiapk.com']

    def __init__(self,start=1,end=2):
        self.prefix_url="http://apk.hiapk.com/apps?sort=5&pi="
        self.base_url="http://apk.hiapk.com"
        self.prefix_path="../temp/"
        self.page_start=int(start)
        self.page_index=self.page_start
        self.page_end=int(end)
        HiapkSpider.start_urls=[self.prefix_url+str(self.page_start)]

    def parse(self,response):
        self.apkList=[]
        if self.page_index > self.page_end:
            self.log('Spider Ends')
            return
        self.log('Crawl '+str(self.page_index)+' starts')
        for sel in response.xpath('//li[contains(@class,"list_item")]'):
            item=ApkItem()
            item['name']=sel.xpath('div/dl/dt/span/a/@href').extract()[0].split('.')[-1]
            item['version']=sel.xpath('div/dl/dt/*[2]/text()').extract()[0][1:-1]
            item['url']=self.base_url+sel.xpath('div/*[3]/a/@href').extract()[0]
            item['path']=self.prefix_path+item['name']+'.apk'
            self.apkList.append(item)
        self.download()
        self.page_index+=1
        for item in self.apkList:
            yield item
        yield Request(self.prefix_url+str(self.page_index),
                      callback=self.parse)


    def download(self):
        self.log('Download for page '+str(self.page_index)+' starts')
        p=Pool()
        result=[]
        for item in self.apkList:
           self.log('Download for apk '+item['name']+' starts')
           tmp=p.apply_async(urllib.urlretrieve,[item['url'],item['path']])
           result.append(tmp)
        p.close()
        p.join()
        self.log('Download for page '+str(self.page_index)+' ends')

        for i in range(0,len(self.apkList)):
            tmp=self.apkList[i]
            try:
                result[i].get()
            except:
                self.log('Download for apk '+tmp['name']+' fails')
                tmp['downloaded']=False
                os.remove(tmp['path'])
                continue
            else:
                tmp['downloaded']=True
