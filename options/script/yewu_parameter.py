#!/usr/bin/python
# coding: utf-8
import sys
import urllib2
import time
from datetime import datetime
from bs4 import BeautifulSoup

TODAY=datetime.today().strftime('%Y%m%d')

def getDataOnDate(ts):
	t=0;
	alldata=[]
	while True:
		time.sleep(1)
		try:
			req=urllib2.Request('http://www.dce.com.cn/PublicWeb/MainServlet?action=Pu00121_result&Pu00121_Input.trade_date=%s&Pu00121_Input.variety=all'%ts)
			req.add_header('user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
			url=urllib2.urlopen(req,timeout=5)
			data=url.read()
			soup=BeautifulSoup(data,from_encoding='utf-8')
			for i,prod in enumerate(soup.find('table').find('table').find_all('tr')):
				#skip first name line
				if i>0:
					tmplist=[('%s'%(col.text.replace(',','').strip())).encode('utf8') for col in prod.find_all('td')]
					tmplist.append(ts)
					tmplist.append(TODAY)
					alldata.append(tmplist)
			return alldata
		except urllib2.HTTPError as e:
			print '%s->Data not exist on date:%s'%(e.code,ts)
			return None
		except Exception as e:
			print 'Error on date:%s\n%s'%(ts,e)
			t+=60
			if t>70:
				break
			time.sleep(t)

if __name__=='__main__':
	with file(sys.argv[2],'a') as output:
		alldata=getDataOnDate(sys.argv[1])
		if alldata is not None and len(alldata)>0:
			for prod in alldata:
				output.write('\001'.join(prod))
				output.write('\n')
				output.flush()
