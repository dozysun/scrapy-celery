#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'

import urllib
import urllib2

url = ' http://www.dianping.com/shop/6054444'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'name' : 'WHY',
          'location' : 'SDU',
          'language' : 'Python' }

headers = { 'User-Agent' : user_agent }
data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page