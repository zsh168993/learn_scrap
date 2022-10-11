import scrapy
from zhonghua.items import WebAttributesItem,WebPricesItem,ImageItem,ProductInformationItem,PriceItem
from zhonghua.spiders.Info import Price_Info
from scrapy_redis.spiders import RedisSpider  #导入RedisSpider
from collections import defaultdict
import math
import json



class LabgogoSpider(RedisSpider):
    name = 'labgogo'
    allowed_domains = ['www.labgogo.com']

    redis_key = 'biochemsafebuy:start_urls'  # 开启爬虫钥匙
    def start_requests(self):
        urls=[
            "https://www.labgogo.com/product/prolist_132.html",
            "https://www.labgogo.com/product/prolist_133.html",
            "https://www.labgogo.com/product/prolist_436.html",
            "https://www.labgogo.com/product/prolist_134.html",
            "https://www.labgogo.com/product/prolist_135.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse, meta={'product_url': url}, dont_filter=True)

    def parse(self, response):
        product_node_list = response.xpath("//*[@id='myform']/div//table//tr/td[3]/a")
       # cas_num = response.xpath("//*[@id='myform']/div//table//tr/td[3]/a/span[2]/text")
        for product_node in product_node_list:
            product_url = "https://www.labgogo.com" + product_node.xpath("./@href").get()#https://www.labgogo.com/product/productnew_53696.html
            cas = product_node.xpath("./span[2]/text()").get()
            yield scrapy.Request(product_url, callback=self.product_parse, meta={'product_url': product_url})  #######
            pid = product_node.xpath("./@href").get().replace("/product/productnew_","").replace(".html","")
            data = {"pid": pid,"pinpai":"","baozhuan":"","price":"", "cas": cas, "page": str(1)}
            url = "http://www.labgogo.com/product/ProductNew.aspx/GetTbsp"
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image,application/json',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Sec - Fetch - Dest': "document",
                       'Referer':product_url,
                       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                       'Content-Type': 'application/json; charset=utf-8'}
            yield scrapy.Request(url=url, method="POST", body=json.dumps(data), headers=headers, callback=self.price_parse,
                                 meta={"product_url":product_url
                                       ,"pid" :pid,"cas": cas,"data":data,"url":url,"headers":headers})
        #next_page
        page_urls = response.xpath("//*[@id='AspNetPager1']/a")
        for page_url in page_urls:
            page_url_flag = page_url.xpath("string(.)").get()
            if page_url_flag == "尾页":
               page_url_last = "https://www.labgogo.com/product/" + page_url.xpath("./@href").get()
        for page_url in page_urls:
            page_url_flag = page_url.xpath("string(.)").get()
            if page_url_flag == "下一页":
                #https://www.labgogo.com/product/prolist.aspx?classid=132&page=2
                next_page_url = "https://www.labgogo.com/product/" + page_url.xpath("./@href").get()
                if next_page_url == page_url_last:
                    print("最后一页网址： " + next_page_url)
                    yield scrapy.Request(next_page_url, callback=self.parse, dont_filter=True)
                    break
                else:
                    yield scrapy.Request(next_page_url, callback=self.parse, dont_filter=True)
            else:
                continue

    def err_back(self, response):
        print("response:", response)
        print("request:", response.request)
        print(response.request.headers)

    def product_parse(self, response):

        # 产品信息
        productin_formation_item = ProductInformationItem()
        product_information = defaultdict(dict)
        product_node = response.xpath("//*[@id='myform']/div/div/div/p")
        cas_num = product_node.xpath("./span[1]").xpath("string(.)").get()
        product_information[cas_num]["MDL"] = product_node.xpath("./span[2]").xpath("string(.)").get()
        product_information[cas_num]["分子式"] = product_node.xpath("./span[3]/text()").get().replace(" ","")
        product_information[cas_num]["分子量"] = product_node.xpath("./span[4]/text()").get()
        productin_formation_item["product_information"] = product_information
        yield productin_formation_item

        # 保存网页
        web_attributes_item = WebAttributesItem()
        web_attributes_item["web_attributes_response"] = response.text
        web_attributes_item["web_item_cas"] = cas_num
        yield web_attributes_item
        # 保存图片
        image_item = ImageItem()
        image_item['image_name'] = cas_num + str(".jpg")
        image_item['image_source'] = response.xpath("//*[@id='imgMain']/@src").get()
        yield image_item
    def price_info_get(self,price,prices,product_prices):
        for product_price in product_prices:
            # 品牌
            price.brand = product_price["PingPai"]
            # 货号
            price.art_no = product_price["YuanShi"]
            # 品名
            price.chinese_name = product_price["ProChaName"]
            price.english_name = product_price["EnglishName"]
            # 规格纯度
            price.specification_pureness = product_price["ChunDu"]
            # 包装
            price.packaging = product_price["BaoZhuan"]
            # 牌价含税
            price.price = product_price["Pprice"]
            price.price = float(price.price.strip())

            price.deal_price = product_price["DealPrice"]
            price.deal_price = float(price.deal_price.strip())
            prices[product_price["Cas"]].append(
                [price.brand, price.art_no, price.chinese_name, price.english_name, price.specification_pureness,
                 price.packaging, price.price, price.deal_price])

        return prices

    def response_parse_other_page(self, response):

        price_item=response.meta["price_item"]
        prices = response.meta["prices"]
        page = response.meta["page"]
        page_index = response.meta["page_index"]
        cas = response.meta["cas"]
        price = response.meta["price"]

        web_price_item = WebPricesItem()
        web_price_item["web_prices_response"] = response.text
        web_price_item["web_item_cas"] = cas
        web_price_item["web_item_cas_page"] = cas + "_page"+str(page_index)
        yield web_price_item
        product_prices = json.loads(response.text)["d"]["listSpec"]
        if product_prices==None:
            print(123)
        prices = self.price_info_get(price, prices, product_prices)
        if page_index == page:
            prices[cas].append(response.meta['product_url'])
            price_item["price_item"] = prices
            yield price_item
    # 价格信息
    def price_parse(self, response):
        prices = defaultdict(list)
        price_item = PriceItem()

        #{"__type":"TBSpec","Sid":1641535,"DealPrice":"108.8","ShowPromotion":"促","YuanShi":"C6083-10g","HotSpec":1641535,
        # "ProChaName":"铬天青S","EnglishName":"Chromeazurol S",
        # "Cas":"1667-99-8","BaoZhuan":"10g","CuxiaoPrice":"","Pprice":"136.00","PingPai":"Macklin","ChunDu":"生物技术级","Shku":"5","Bfku":"5"}
        price = Price_Info()
        try:
            page = math.ceil(int(json.loads(response.text)["d"]["pageNum"]) / 30)
        except:
            page = 1
        pid = response.meta["pid"]
        cas = response.meta["cas"]
        url =response.meta["url"]
        product_url = response.meta['product_url']
        headers = response.meta["headers"]
        #
        web_price_item = WebPricesItem()
        web_price_item["web_prices_response"] = response.text
        web_price_item["web_item_cas"] = cas
        web_price_item["web_item_cas_page"] = cas+"_page"+"1"
        yield web_price_item


        product_prices = json.loads(response.text)["d"]["listSpec"]
        if product_prices==None:
            print(123)
        prices = self.price_info_get(price, prices, product_prices)

        if page == 1:
            prices[cas].append(response.meta['product_url'])
            price_item["price_item"] = prices
            yield price_item
        else:
            for page_index in range(2, page + 1):
                data = {"pid": pid, "pinpai": "", "baozhuan": "", "price": "", "cas": cas, "page": str(page_index)}
                yield scrapy.Request(url=url, method="POST", body=json.dumps(data), callback = self.response_parse_other_page,
                                     headers=headers,meta={"price_item":price_item,"prices":prices,"product_url":product_url,
                                                           "price":price,"page":page,"cas":cas,"page_index":page_index})







