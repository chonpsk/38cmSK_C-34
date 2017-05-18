# -*- coding: UTF-8 -*-

import requests
import time
import random

view_link = 'http://www.spinns.com/sb69_25spinns/'
vote_link = 'http://www.spinns.com/sb69_25spinns/vote.php'

tot = 82

def vote(prx):
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
	

ip = 'http://www.cybersyndrome.net/plr.html'

while True:
	rqst = requests.get(ip)
	s = str(rqst.text.encode('utf-8'))
	pos = 0
	for i in range(1, 404):
		pos = s.find('>' + str(i) + '</td><td>', pos)
		pos += 10 + len(str(i))
		nxt = s.find('<', pos)
		if s[pos:nxt].find(':', 0) == -1 or nxt - pos > 20:
			break
		vote(s[pos:nxt])
		pos = nxt
	time.sleep(900)
