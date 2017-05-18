# -*- coding: UTF-8 -*-

import requests
import time
import random

view1 = 'https://sanriocharacterranking.com'
view2 = 'https://sanriocharacterranking.com/characters/'
view_link = 'https://sanriocharacterranking.com/questionnaire/?cid=showbyrock'
vote_link = 'https://sanriocharacterranking.com/vote/?cid=showbyrock'
rakuten = 'http://event.rakuten.co.jp/sanrio/?scid=we_ich_smt_sanrio_webclip_2017_008'

tot = 0
rtot = 0

def vote(prx):
    prx = prx[:-1]
    print (prx + '    ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    s = requests.Session()
    s.proxies = {'http': prx}
    try:
        s.get(view1, timeout = 1)
        s.get(view2, timeout = 1)
        s.get(view_link, timeout = 1)
    except:
        return
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
    except:
        return
    print (r.url)
    if r.url.find('vote', 0) != -1:
        global tot
        tot = tot + 1
    print ('vote ' + str(tot))
    try:
        requests.get(rakuten, headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36'}, proxies = {'http': prx}, timeout = 1)
    except:
        return
    global rtot
    rtot += 1
    print ('rakuten ' + str(rtot))
	

ip = 'http://api.xicidaili.com/free2016.txt'

while True:
	try:
		rqst = requests.get(ip)
	except:
		time.sleep(4)
	fl = open('ipp', 'w')
	print (rqst.text, file = fl)
	print ('', file = fl)
	fl.close()
	fl = open('ipp', 'r')
	for i in range(0, 100):
		vote(fl.readline())
#		fl.readline()
#    time.sleep(random.randint(3, 7))
	fl.close()
#	time.sleep(600)
