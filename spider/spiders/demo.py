#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'

from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import Selector
from spider.items import DmozItem

class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul[@class="directory-url"]/li')
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('text()').extract()
            items.append(item)
        return items

# class MySpider(CrawlSpider):
#     name = '58'
#     allowed_domains = ['58.com']
#     start_urls = ['http://sh.58.com/xiaoqu/']
#     # start_urls = ['http://sh.58.com/xiaoqu/%s' % str(x) for x in [1399,1400,1403,1401,1411,1402,1406,1407,1404,1405,6179,6180,6961,6962,6963,6965,6977,6978,6979]]
#     settings = {}
#     rules = (
#         # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
#         # Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),
#
#         # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
#         Rule(LinkExtractor(allow=(r'/pn_\d+/', )), callback='parse_item', follow=True),
#         Rule(LinkExtractor(allow=(r'^http://sh.58.com/xiaoqu/$', )), callback='parse_item', follow=False),
#     )
#
#     @count_method
#     def parse_item(self, response):
#         return
#         name = response.xpath('//li[@class="tli1"]/a/text()').extract()
#         address = response.xpath('//li[@class="tli2"]/text()').extract()
#         if name and address:
#             create_community.apply_async(args=[name,address])

# import urllib
# import urllib2
#
# url = 'http://www.someserver.com/register.cgi'
#
# values = {'name' : 'WHY',
#           'location' : 'SDU',
#           'language' : 'Python' }
#
# data = urllib.urlencode(values) # 编码工作
# req = urllib2.Request(url, data)  # 发送请求同时传data表单
# response = urllib2.urlopen(req)  #接受反馈的信息
# the_page = response.read()  #读取反馈的内容
#

#scrapy crawl demo -o data.json