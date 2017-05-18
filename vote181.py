# -*- coding: UTF-8 -*-

import requests
import time
import random

view_link = 'https://sanriocharacterranking.com/questionnaire/?cid=showbyrock'
vote_link = 'https://sanriocharacterranking.com/vote/?cid=showbyrock'
rakuten = 'http://event.rakuten.co.jp/sanrio/?scid=we_ich_smt_sanrio_webclip_2017_008'

tot = 0

def vote(prx):
    prx = prx[:-1]
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
	fl = open('ip181', 'w')
	try:
		rqst = requests.get(ip)
	except:
		continue
	print (rqst.text.encode('utf-8'), file = fl)
	fl.close()
	fl = open('ip181', 'r')
	rq = fl.readline()
	fl.close()
	rq = rq.replace(' ', '')
	i = rq.find('<tdwidth="385">', 0)
	fl = open('ip181', 'w')
	while True:
		i = rq.find('\\r\\n<td>', i)
		if i == -1:
			break
		s = rq[rq.find('>', i) + 1: rq.find('<', i + 9)] + ':'
		i = rq.find('<td>', i + 9)
		s = s + rq[rq.find('>', i) + 1: rq.find('<', i + 4)]
		print (s, file = fl)
	fl.close()
	fl = open('ip181', 'r')
	for i in range(0, 100):
		vote(fl.readline())
		fl.readline()
	fl.close()
