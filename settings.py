# -*- coding: utf-8 -*-

# Scrapy settings for spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spider (+http://www.yourdomain.com)'


#celery配置信息
#broker, backend
BACKEND_URL = 'redis://127.0.0.1:6379/10'

# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = 'redis://127.0.0.1:6379/11'

#Database : Mysql
ENGINE="mysql://root:111111@127.0.0.1:3306/decorate?charset=utf8"

