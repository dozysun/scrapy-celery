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


# spider setting
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'
CONCURRENT_REQUESTS_PER_DOMAIN = 1 #单个网站并发数
# CONCURRENT_REQUESTS = 1 #并发请求个数
# COOKIES_ENABLES=False  #进cookie

# 优先策略 默认lifo 深度优先
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

RANDOMIZE_DOWNLOAD_DELAY = True #随机 1- 1.5延迟
DOWNLOAD_DELAY = 1    # seconds of delay
DEFAULT_REQUEST_HEADERS = {
    'Accept':'application/json, text/javascript',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    # 'Cookie':'_hc.v="\"38251787-3c72-42c1-b9b5-a00036cef909.1422948121\""; _tr.u=2lZhjrUmyCCQ0PO7; _adwp=256526943.0896806990.1426602011.1426602011.1426843729.2; _adwr=87910621%23http%253A%252F%252Fele.me%252Fprofile%252Forder; cityid=1; PHOENIX_ID=0a016731-14d701b401e-4dd23b; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1431913475,1431915946,1431916016; Hm_lpvt_dbeeb675516927da776beeb1d9802bd4=1432173800; JSESSIONID=AD03E1DB729372B20DA64FC228AEE182; aburl=1; cy=1; cye=shanghai',
    'Pragma':'no-cache',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    'X-Request':'JSON',
    'X-Requested-With':'XMLHttpRequest',
}



#celery配置信息
#broker, backend
BACKEND_URL = 'redis://127.0.0.1:6379/10'

# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = 'redis://127.0.0.1:6379/11'

#Database : Mysql
ENGINE="mysql://root:111111@127.0.0.1:3306/decorate?charset=utf8"

