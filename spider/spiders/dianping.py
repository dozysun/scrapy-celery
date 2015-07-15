#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'

import time
import random
from utils import count_method
import scrapy
from scrapy.selector import Selector
from celery_tasks.tasks import create_company_test,create_company_from_dianping_all

class MySpiders(scrapy.Spider):
    name = 'dianping2'
    allowed_domains = ['www.dianping.com']
    # start_urls = ['http://www.dianping.com/search/category/1/90/g25475p1']
    start_urls = ['http://www.dianping.com/search/category/%s/90/g25475p1' % x for x in range(1033,3000)]

    def parse(self, response):
        sel = Selector(response)
        #获取店铺详细页信息
        for url in sel.xpath('//li/a/@href').re(r'^(/shop/\d+)$'):
            url = 'http://www.dianping.com' + url
            yield scrapy.Request(url, callback=self.parse_data)
            time.sleep(random.randint(2,4))

        #获取下一个list页
        next_url = sel.xpath('//div[@class="pages"]/a/@href').extract()
        if next_url:
            next_url = 'http://www.dianping.com' + next_url[-1].split('?')[0]
            yield scrapy.Request(next_url, callback=self.parse)

    @count_method
    def parse_data(self, response):
        print response.url
        sel = scrapy.Selector(response)

        kwargs = {
        'city': sel.xpath('//a[@class="city J-city"]/text()').extract(),
        'title': sel.xpath('//h1[@class="shop-title"]/text()').extract(),
        'area': sel.xpath('//a[@class="region"]/text()').extract(),
        'addr': sel.xpath('//div[@class="shop-addr"]/span/@title').extract(),
        'phone': sel.xpath('//div[@class="shopinfor"]/p/span/text()').extract(),
        'desc': sel.xpath('//table/tbody/tr/td/div/text()').extract(),
        'photo': sel.xpath('//div[@class="mainpic J_large"]/a/img/@src').extract(),
        }

        if not kwargs['addr'] and not kwargs['phone']:
            kwargs['city'] = sel.xpath('//div[@class="location"]/a/span/text()').extract()
            kwargs['area'] = sel.xpath('//span[@class="region"]/text()').extract()
            kwargs['addr'] = sel.xpath('//span[@itemprop="street-address"]/text()').extract()
            kwargs['phone'] = sel.xpath('//strong[@itemprop="tel"]/text()').extract()
            kwargs['photo'] = sel.xpath('//img[@itemprop="photo"]/@src').extract()

        if not kwargs['addr'] or not kwargs['phone']:
            #保存仍然无法获取area和addr的地址
            save_dict = {
                'title': kwargs['title'][0].encode('utf-8'),
                'url':  response.url
            }
            f = open('dianping_company', 'awr')
            f.writelines('{"url":"%s","title":"%s"}\n' % (save_dict['url'],save_dict['title']))
            # f.writelines(str(save_dict)+'\n')
            f.close()

        # print kwargs
        create_company_from_dianping_all.apply_async(kwargs=kwargs)
        return


