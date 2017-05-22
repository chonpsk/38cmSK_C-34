"""
-------------------------------------------------
    File Name:     proxyGetter.py
    Description:   代理抓取模块，负责与网络的交互。
                   注意，代理网站的HTML结构可能会时常的更新，
                   会导致本文件下的抓取函数失效，所以，在运行
                   代理池之前，需要更新一下FreeProxyGetter类
                   中以crawl_开头的方法。
    Author:        Liu
    Edited by:     chonps
-------------------------------------------------
"""

import time
import requests
import re

from .utils import get_page
from .setting import *

class ProxyMetaclass(type):
    """
    爬虫的元类，在FreeProxyGetter类中加入
    __CrawlFunc__和__CrawlFuncCount__
    两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    """
    代理爬虫，负责扫描各大代理网站，抓取代理。
    该类有可扩展性，可根据需要自己添加新站点的代理抓取函数，
    但是函数名必须以crawl_开头，返回值必须以"host:port"的形式返回，
    添加器会自动识别并调用此类函数。
    """
    
    def get_raw_proxies(self, callback, count = GET_NUMBER):
        proxies = []
        try:
            for proxy in eval("self.{}()".format(callback)):
                proxies.append(proxy)
                if len(proxies) >= count:
                    break
        except:
            pass
        print ('get ' + str(len(proxies)) + ' proxies')
        return proxies

    def crawl_kuaidaili(self, page_count=8):
        """
        抓取快代理网的数据
        """
        start_url = 'http://www.kuaidaili.com/proxylist/{}/'
        print (start_url)
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            try:
                soup = get_page(url) 
            except:
                continue
      
            proxy_list = soup.find('div', {'id': 'index_free_list'}).find('tbody')
            for proxy in proxy_list.find_all('tr'):
                ip = proxy.find_all('td')[0].get_text()
                port = proxy.find_all('td')[1].get_text()
                yield ':'.join([ip, port])


    def crawl_xici(self):
        """
        抓取xici代理网的数据。
        """
        start_url = 'http://api.xicidaili.com/free2016.txt'
        print (start_url)
        try:
            soup = get_page(start_url)
        except:
            return
        proxy_list = soup.find('p') 
        return proxy_list.get_text().split('\r\n')
    
    def crawl_proxy360(self):
        """
        抓取proxy360网的数据。
        """
        start_url = 'http://www.proxy360.cn/default.aspx'
        print (start_url)
        try:
            soup = get_page(start_url)
        except:
            return
        for proxy in soup.find_all('div', {"class": "proxylistitem"}):
            item = proxy.find_all('span', {"class": "tbBottomLine"})
            ip = item[0].get_text().replace('\r\n', '').replace(' ', '')
            port = item[1].get_text().replace('\r\n', '').replace(' ', '')
            yield ':'.join([ip, port])


    def crawl_ip181(self):
        start_url = 'http://www.ip181.com'
        print (start_url)
        try:
            soup = get_page(start_url)
        except:
            return
        proxy_list = soup.find('table').find('tbody')
        for proxy in proxy_list.find_all('tr'):
            ip = proxy.find_all('td')[0].get_text()
            if ip.find('.') != -1:
                port = proxy.find_all('td')[1].get_text()
                yield ':'.join([ip, port])

    def crawl_kxdaili(self):
        start_url = 'http://www.kxdaili.com/ipList/{}.html'
        print (start_url)
        urls = [start_url.format(page) for page in range(1, 11)]
        for url in urls:
            try:
                soup = get_page(url)
            except:
                return
            proxy_list = soup.find('table', class_ = ['ui', 'table', 'segment']).find('tbody')
            for proxy in proxy_list.find_all('tr'):
                ip = proxy.find_all('td')[0].get_text()
                port = proxy.find_all('td')[1].get_text()
                yield ':'.join([ip, port])

    def crawl_89ip(self):
        start_url = 'http://www.89ip.cn'
        print (start_url)
        soup = get_page(start_url)
        url = 'http://www.89ip.cn/api/?&tqsl=' + soup.find('span', class_ = ['STYLE30']).get_text(strip = True) + '&sxa=&sxb=&tta=&ports=&ktip=&cf=1'
        try:
            soup = get_page(url)
        except:
            return
        return re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', soup.get_text('|'))

    def crawl_goubanjia(self):
        start_url = 'http://www.goubanjia.com/index{}.shtml'
        print (start_url)
        urls = [start_url.format(page) for page in range(1, 11)]
        for url in urls:
            try:
                soup = get_page(url)
            except:
                return
            proxy_list = soup.find('table', {"class": "table"}).find('tbody')
            for tr in proxy_list.find_all('tr'):
                _proxy = tr.find('td').find_all(['span', 'div'])
                proxy = [i.get_text() for i in _proxy]
                proxy = proxy[:-1]
                proxy.append(':')
                proxy.append(tr.find('td').find('span', class_ = ['port']).get_text())
                yield ''.join(proxy)

    def crawl_coobobo(self):
        start_url = 'http://www.coobobo.com/free-http-proxy/{}'
        print (start_url)
        urls = [start_url.format(page) for page in range(1, 11)]
        for url in urls:
            try:
                soup = get_page(url)
            except:
                return
            proxy_list = soup.find('table', {"class": "table"}).find('tbody')
            for tr in proxy_list.find_all('tr'):
                proxy = re.findall(r'"\S+"|\'\S+\'', tr.find_all('td')[0].get_text())
                proxy = [s[1:-1] for s in proxy]
                proxy.append(':')
                proxy.append(tr.find_all('td')[1].get_text())
                yield ''.join(proxy)

    def crawl_free_proxy_list(self):
        start_url = 'https://free-proxy-list.net'
        print (start_url)
        try:
            soup = get_page(start_url)
        except:
            return
        proxy_list = soup.find('table').find('tbody')
        for proxy in proxy_list.find_all('tr'):
            ip = proxy.find_all('td')[0].get_text()
            port = proxy.find_all('td')[1].get_text()
            yield ':'.join([ip, port])

    def crawl_66ip(self):
        start_url = 'http://www.66ip.cn/pt.html'
        print (start_url)
        soup = get_page(start_url)
        url = 'http://www.66ip.cn/mo.php?sxb=&tqsl=' + [text for text in soup.find('table',  border = '0').find('span').stripped_strings][1] + '&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1'
        try:
            soup = get_page(url)
        except:
            return
        return re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', soup.get_text('|'))

