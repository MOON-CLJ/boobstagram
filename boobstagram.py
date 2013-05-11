# -*- coding: utf-8 -*-

import eventlet
from eventlet.green import urllib2
from lxml import etree
import os

base_url = 'http://boobstagram.com/category/boobs/page/%s/'
pool = eventlet.GreenPool(10)


def filter_url(urls):
    _urls = []
    for url in urls:
        if os.path.exists(url[url.rfind('/') + 1:]):
            # 当碰到大量existed，说明没有更多内容，请ctrl+c停止脚本
            print 'existed'
        else:
            _urls.append(url)
    return _urls


def fetch(url):
    print 'opening', url
    try:
        body = urllib2.urlopen(url).read()
        print 'done with', url
        return url, body
    except Exception:
        print 'forbidden', url
        return url, None

page = 1
while 1:
    body = urllib2.urlopen(base_url % page).read()
    hxs = etree.HTML(body)
    urls = hxs.xpath('//div[@id="wrapper"]//div[@class="entry"]/figure/a/@name')
    urls = filter_url(urls)

    for url, body in pool.imap(fetch, urls):
        if body:
            f = open(url[url.rfind('/') + 1:], 'w')
            print 'write ' + url
            f.write(body)
            f.close()
    print 'goto next [page: %s]' % page
    page += 1
