# -*- coding: UTF-8 -*-

import requests
import time
import random

view_link = 'http://www.spinns.com/sb69_25spinns/'
vote_link = 'http://www.spinns.com/sb69_25spinns/vote.php'

tot = 0

def vote(prx):
    prx = prx[:-1]
    print (prx + '    ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    s = requests.Session()
    s.proxies = {'http': prx}
    try:
        s.get(view_link, timeout = 9)
    except:
        return
    payload = {'q_id.x': random.randint(1, 126),
               'q_id.y': random.randint(1, 15),
               'q_id': 15}
    hh = {'Referer': view_link,
          'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    try:
        r = s.post(vote_link, data = payload, headers = hh, timeout = 9)
    except:
        return
    print (r.url)
    if r.url.find('complete.html', 0) != -1:
        global tot
        tot = tot + 1
    print ('vote ' + str(tot))

ip1 = 'http://www.kuaidaili.com/free/outtr/'
ip2 = 'http://www.kuaidaili.com/free/outha/'
ip3 = 'http://www.kuaidaili.com/free/intr/'
ip4 = 'http://www.kuaidaili.com/free/inha/'

def getip(url, fl):
	rqst = requests.get(url)
	i = 0
	while True:
		i = rqst.text.find('"IP"', i)
		if i == -1:
			break
		s = rqst.text[rqst.text.find('>', i) + 1: rqst.text.find('<', i)]
		i = rqst.text.find('"PORT"', i)
		s = s + ':'
		s = s + rqst.text[rqst.text.find('>', i) + 1: rqst.text.find('<', i)]
		print (s, file = fl)


while True:
	fl = open('ipk', 'w')
	getip(ip1, fl)
	getip(ip2, fl)
	getip(ip3, fl)
	getip(ip4, fl)
	print ('', file = fl)
	fl.close()
	fl = open('ipk', 'r')
	for i in range(0, 60):
		vote(fl.readline())
#    time.sleep(random.randint(3, 7))
	fl.close()
#	time.sleep(444)
