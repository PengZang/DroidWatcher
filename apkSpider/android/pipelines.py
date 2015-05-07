# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
import pickle
# class PermissionPipeline(object):
#     def __init__(self):
#         self.file=open('../temp/permission.pk','wb')
#         self.data=[]
#     def process_item(self,item,spider):
#         if item['permission']:
#             self.data.append(item['permission'])
#         else:
#             raise DropItem("Missing Content ")
#     def close_spider(self,spider):
#         print self.data
#         pickle.dump(self.data,self.file)
#         self.file.close()
#
# class apkPipeline(object):
#     def __init__(self):
#         self.file=open('../temp/apkList.pk','wb')
#         self.data=[]
#     def process_item(self,item,spider):
#         self.data.append(item)
#     def close_spider(self,spider):
#         print self.data
#         pickle.dump(self.data,self.file)
#         file.close()


class myPipeline(object):
    def open_spider(self,spider):
        if spider.name=='permission':
            self.file=open('../temp/permission.pk','wb')
            self.data=[]
            return
        if spider.name=='hiapk':
            self.file=open('../temp/apkList.csv','a')
            return
    def process_item(self,item,spider):
        if spider.name=='permission':
            if item['permission']:
                self.data.append(item['permission'])
                return item
            else:
                raise DropItem('Missing Content')
        if spider.name=='hiapk':
            if item['downloaded']:
                self.file.write(item['name']+','+item['version']+','
                                +item['path']+','+item['url']+'\n')
                return item
            else:
                raise DropItem('Download failed')

    def close_spider(self,spider):
        if spider.name=='permission':
            pickle.dump(self.data,self.file)
        self.file.close()