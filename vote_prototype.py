# -*- coding: UTF-8 -*-

import requests
import time
import random
import re
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

view_link = 'https://sanriocharacterranking.com/questionnaire/?cid=showbyrock'
vote_link = 'https://sanriocharacterranking.com/vote/?cid=showbyrock'
rakuten = 'http://event.rakuten.co.jp/sanrio/?scid=we_ich_smt_sanrio_webclip_2017_008'

tot = 0

def get_page(url):
    try:
        r = requests.get(url, headers = headers)
    except:
        raise
    try:
        soup = BeautifulSoup(r.content.decode("utf-8"), 'lxml')
    except UnicodeDecodeError:
        soup = BeautifulSoup(r.text, 'lxml')
    return soup

def vote(prx):
    print (prx + '    ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    s = requests.Session()
    s.proxies = {'http': prx}
    payload = {'age': random.randint(20, 29),
               'gender_id': random.randint(1, 2),
               'pref_id': random.randint(1, 47),
               'agreement': 'on'}
    hh = {'Referer': view_link,
          'Origin': 'https://sanriocharacterranking.com',
          'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    try:
        r = s.post(vote_link, data = payload, headers = hh, timeout = 1)
        requests.get(rakuten, headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36'}, proxies = {'http': prx}, timeout = 1)
    except:
        return
    try:
        requests.get('http://127.0.0.1:1025/add/?proxy={}'.format(prx))
    except:
        pass
    print (r.cookies.get_dict())
    print (r.url)
    if r.url.find('vote', 0) != -1:
        global tot
        tot = tot + 1
    print ('vote ' + str(tot))

def getIP(url):
    print (url)
    try:
        soup = get_page(url)
    except:
        raise
    proxy_list = soup.find('table').find('tbody')
    for proxy in proxy_list.find_all('tr'):
        ip = proxy.find_all('td')[0].get_text()
        port = proxy.find_all('td')[1].get_text()
        print(':'.join([ip, port]))

    """
    proxy_list = soup.find('table', class_ = ['ui', 'table', 'segment']).find('tbody')
    for proxy in proxy_list.find_all('tr'):
        ip = proxy.find_all('td')[0].get_text()
        port = proxy.find_all('td')[1].get_text()
        vote(':'.join([ip, port]))
    """


start_url = 'http://www.66ip.cn/pt.html'
#start_url = 'http://www.66ip.cn/mo.php?sxb=&tqsl=6805&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1'
soup = get_page(start_url)
#print ([text for text in soup.find('table', border = '0').find('span').stripped_strings])
url = 'http://www.66ip.cn/mo.php?sxb=&tqsl=' + [text for text in soup.find('table',  border = '0').find('span').stripped_strings][1] + '&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1'
print (url)
soup =  get_page(url)
print (re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', soup.get_text('|')))
#getIP(start_url)
