# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from itemadapter import ItemAdapter
import os
import json
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from zhonghua.items import ProductInformationItem,PriceItem,ImageItem,WebAttributesItem,WebPricesItem

from zhonghua import settings

#

class ZhonghuaImagesPipLine(ImagesPipeline):
    def get_media_requests(self, image_item, info):
        if type(image_item) == ImageItem:
            image_item=ItemAdapter(image_item)
            yield scrapy.Request(url=image_item['image_source'], meta={'image_item': image_item})

    def file_path(self, request, response=None, info=None):
        filePath = request.meta['image_item']['image_name']
        return filePath

    def item_completed(self, results, item, info):
        return item

class ZhonghuaWebWriterPipeline:
    def open_spider(self, spider):
        if spider.name == 'labgogo':
            if os.path.exists(settings.PROJECT_ROOT+'/WEBFILE/'):
                pass
            else:
                os.mkdir(settings.PROJECT_ROOT+'/WEBFILE/')

    def process_item(self, item, spider):
        if spider.name == 'labgogo':
            #WebAttributesItem,WebPricesItem

            if type(item) == WebAttributesItem:
                if os.path.exists(settings.PROJECT_ROOT + '/WEBFILE/' + item["web_item_cas"]):
                    pass
                else:
                    os.mkdir(settings.PROJECT_ROOT + '/WEBFILE/' + item["web_item_cas"])
                with open(settings.PROJECT_ROOT+'/WEBFILE/'+item["web_item_cas"]+"/attributes_{}.htm".format(item["web_item_cas"]), mode='w', encoding='UTF-8') as file:
                    file.write(item["web_attributes_response"])
            if type(item) == WebPricesItem:
                if os.path.exists(settings.PROJECT_ROOT + '/WEBFILE/' + item["web_item_cas"]):
                    pass
                else:
                    os.mkdir(settings.PROJECT_ROOT + '/WEBFILE/' + item["web_item_cas"])
                with open(settings.PROJECT_ROOT+'/WEBFILE/'+item["web_item_cas"]+"/price_{}.htm".format(item["web_item_cas_page"]), mode='w', encoding='UTF-8') as file:
                    file.write(item["web_prices_response"])
        return item

class ZhonghuaJsonWriterPipeline:
    def open_spider(self, spider):
        if spider.name == 'labgogo':
            if os.path.exists(settings.PROJECT_ROOT+'/JSONFILE'):
                self.price_file = open(settings.PROJECT_ROOT+'/JSONFILE/price_file.json', 'a', encoding='utf-8')
                self.product_information_file = open(settings.PROJECT_ROOT+'/JSONFILE/product_information_file.json', 'a', encoding='utf-8')
            else:
                os.mkdir(settings.PROJECT_ROOT+"/JSONFILE")  # 创建文件夹
                self.price_file = open(settings.PROJECT_ROOT+'/JSONFILE/price_file.json', 'a', encoding='utf-8')
                self.product_information_file = open(settings.PROJECT_ROOT+'/JSONFILE/product_information_file.json', 'a', encoding='utf-8')

    def close_spider(self, spider):
        if spider.name == 'labgogo':
            self.price_file.close()
            self.product_information_file.close()

    def process_item(self, item, spider):
        if spider.name == 'labgogo':
            if type(item) == PriceItem:
                line=json.dumps(ItemAdapter(item["price_item"]).asdict(), ensure_ascii=False)+"\n"
                self.price_file.write(line)
            if type(item) == ProductInformationItem:
                line=json.dumps(ItemAdapter(item["product_information"]).asdict(), ensure_ascii=False)+"\n"
                self.product_information_file.write(line)
        # 不return的情况下，另一个权重较低的pipeline将不会获得item
        return item

