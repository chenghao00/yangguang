# -*- coding: utf-8 -*-
import scrapy
from yangguang.items import YangguangItem


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&page=1']

    def parse(self, response):
        li_list = response.css('body > div.public-content > div.width-12 > ul.title-state-ul > li')
        for li in li_list:
            item = YangguangItem()
            item['id'] = li.css('.state1::text').extract_first()
            item['title'] = li.css('.state3 .color-hover::text').extract_first()
            item["href"] = 'http://wz.sun0769.com' + li.css('.state3 .color-hover::attr(href)').extract_first()
            item['create_time'] = li.css('.state5::text').extract_first()
            # 解析出对应的连接跳转 并用callback函数进行处理，并用meta传递参数
            yield scrapy.Request(url=item["href"], callback=self.parse_detail, meta={"item": item})

        #实现翻页
        next_url='http://wz.sun0769.com'+response.css('.prov_rota::attr(href)').extract_first()
        print('下一页:'+next_url)
        yield scrapy.Request(url=next_url,callback=self.parse)


    def parse_detail(self, response):
        item = response.meta['item']
        item["content"] = response.css('.details-box pre::text').extract_first()
        item['img'] = response.css('.Picture-img img::attr(src)').extract()
        item['img'] = [i for i in item['img']]
        print(item)
        yield item
