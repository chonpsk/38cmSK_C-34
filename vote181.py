# -*- coding: UTF-8 -*-

import requests
import time
import random
from bs4 import BeautifulSoup

view_link = 'https://sanriocharacterranking.com/questionnaire/?cid=showbyrock'
vote_link = 'https://sanriocharacterranking.com/vote/?cid=showbyrock'
rakuten = 'http://event.rakuten.co.jp/sanrio/?scid=we_ich_smt_sanrio_webclip_2017_008'

tot = 0

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


ip = 'http://www.ip181.com/'

while True:
    try:
        soup = BeautifulSoup(requests.get(ip).text, 'lxml')
    except:
        time.sleep(4)
        continue
    proxy_list = soup.find('table').find('tbody')
    for proxy in proxy_list.find_all('tr'):
        ip = proxy.find_all('td')[0].get_text()
        if ip.find('.') != -1:
            port = proxy.find_all('td')[1].get_text()
            vote(':'.join([ip, port]))
