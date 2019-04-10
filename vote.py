# -*- coding: UTF-8 -*-

import requests
import time
import random

view_link = 'https://sanriocharacterranking.com/questionnaire/?cid=showbyrock'
vote_link = 'https://sanriocharacterranking.com/vote/?cid=showbyrock'
rakuten = 'https://event.rakuten.co.jp/sanrio/?scid=we_ich_smt_sanrio_webclip_2019_009'

sp_headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.90 Mobile Safari/537.36'}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

timeout = 4

tot = 0

def delete(prx):
    """
    if random.uniform(0,,1) >= 0.4444:
        try:
            requests.get('http://127.0.0.1:1025/delete/?proxy={}'.format(prx))
        except:
            pass
    """
    try:
        requests.get('http://127.0.0.1:1025/delete/?proxy={}'.format(prx))
    except:
        pass
    

def vote(prx):
    print (prx + '    ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    sess = requests.Session()
    sess.proxies = {'http': prx}
    try:
        requests.get(rakuten, headers = sp_headers, proxies = {'http': prx}, timeout = timeout)
    except:
        return
    """
    try:
        r = s.post(vote_link, data = payload, headers = hh, timeout = timeout)
    except:
        delete(prx)
        return
    print (r.cookies.get_dict())
    print (r.url)
    if r.url.find('vote', 0) != -1:
        global tot
        tot = tot + 1
    """
    global tot
    tot += 1
    print ('vote ' + str(tot))
    time.sleep(random.randint(1,4))

while True:
    try:
        vote(requests.get('http://127.0.0.1:3969/get/').text)
    except:
        time.sleep(4)
