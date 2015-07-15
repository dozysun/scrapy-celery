#!/usr/bin/env python2.7
#encoding:utf-8
__author__ = 'dozy-sun'

import re

import scrapy
from scrapy.spider import Spider
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from settings import ENGINE
from models.qa_mod import City,CityLink58,Province
from celery_tasks.tasks import create_community,create_community_all
from utils import count_method

class CityLinkSpider(Spider):
    #抓取城市url
    name = '58_city_link'
    allowed_domains = ['58.com']
    start_urls = ['http://www.58.com/ershoufang/changecity/?PGTID=14361650437930.6719480943866074&ClickID=1']
    _db = scoped_session(sessionmaker(bind=create_engine(ENGINE,echo=False),autoflush=True,autocommit=False))

    def parse(self, response):
        links = response.xpath('//a')
        link_list = []
        for l in links:
            link = l.xpath('@href').extract()[0]
            if re.match(r'[\w\W]*\.58\.com\/ershoufang\/', link):
                code = link.split('://')[-1].split('.')[0]
                link = link.replace('ershoufang','xiaoqu').encode('utf-8')
                city = l.xpath('text()').extract()[0].encode('utf-8')
                if city:
                    city_info = self._db.query(City).filter(City.city_name.like('%%%s%%' % city)).first()
                    if not city_info:
                        f = open('city_link_58', 'awr')
                        f.writelines('{"url":"%s","title":"%s"}\n' % (link, city))
                        f.close()
                        link_list.append([code,link,0,'',0,''])
                    else:
                        province_info = self._db.query(Province).filter(Province.id == city_info.father).first()
                        link_list.append([code,link,city_info.id,city_info.city_name,province_info.id,province_info.province_name])
        #写数据库
        self._db.execute(
            CityLink58.__table__.insert(),[{
                'code': links[0],
                'link': links[1],
                'city_id': links[2],
                'city_name': links[3],
                'province_id': links[4],
                'province_name': links[5],
            } for links in link_list]
        )

class CommunityALLSpider(Spider):
    #抓取小区
    name = '58_community'
    allowed_domains = ['58.com']
    start_urls = ['http://sh.58.com/xiaoqu/']
    _db = scoped_session(sessionmaker(bind=create_engine(ENGINE,echo=False),autoflush=True,autocommit=False))

    #城市信息字典
    location_dict = {}
    for location_info in _db.query(CityLink58):
        location_dict[location_info.code] = {
        'city_id':location_info.city_id,
        'province_id':location_info.province_id,
        'code':location_info.code,
        'link': location_info.link
        }

    def parse(self, response):
        self.on_response(response)

        #获取下一个list页
        next_url = response.xpath('//a[@class="next"]/@href').extract()
        if next_url:
            next_url = next_url[0]
            yield scrapy.Request(next_url, callback=self.parse)

        #获取下一个城市
        for k,v in self.location_dict.items():
            yield scrapy.Request(v['link'], callback=self.parse)

        self._db.close()

    @count_method
    def on_response(self,response):
        sites = response.xpath('//ul')
        address_list = []
        #获取list页面的小区信息
        for site in sites:
            name = site.xpath('li[@class="tli1"]/a/text()').extract()
            address = site.xpath('li[@class="tli2"]/text()').extract()
            link = site.xpath('li[@class="tli1"]/a/@href').extract()
            if name and address and link:
                address_list.append((name[0].strip(),address[0].strip(),link[0].strip()))

        #celery 写数据库
        location_info = self.location_dict.get(response.url.split('://')[-1].split('.')[0])
        if location_info:
            create_community_all.apply_async(args=[address_list,location_info['city_id'],location_info['province_id'],location_info['code']])
        else:
            create_community_all.apply_async(args=[address_list, 0, 0, ''])
