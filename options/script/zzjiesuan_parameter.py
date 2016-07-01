#!/usr/bin/python
# coding: utf-8
import sys
import urllib2
import time
from datetime import datetime
from bs4 import BeautifulSoup

TODAY=datetime.today().strftime('%Y%m%d')
IMPORTANT='20101008'

def getDataOnDate(ts):
	t=0;
	alldata=[]
	while True:
		time.sleep(3)
		try:
			if ts>=IMPORTANT:
				print 'http://www.czce.com.cn/portal/DFSStaticFiles/Future/%s/%s/FutureDataClearParams.htm?'%(ts[:4],ts)
				url=urllib2.urlopen(urllib2.Request('http://www.czce.com.cn/portal/DFSStaticFiles/Future/%s/%s/FutureDataClearParams.htm'%(ts[:4],ts)))
			else:
				print 'http://www.czce.com.cn/portal/exchange/%s/dataclearparams/%s.htm'%(ts[:4],ts)
				url=urllib2.urlopen('http://www.czce.com.cn/portal/exchange/%s/dataclearparams/%s.htm'%(ts[:4],ts))
			data=url.read()
			soup=BeautifulSoup(data,from_encoding='utf-8')
                        return soup
			for i,prod in enumerate(soup.find('table').find('table').find_all('tr')):
				#skip first name line
				if i>0:
					tmplist=[('%s'%(col.text)).encode('utf8') for col in prod.find_all('td')]
					if len(tmplist)<9:
						tmplist.append('None')
						tmplist.append('None')
						tmplist.append('None')
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
			time.sleep(t)

if __name__=='__main__':
	with file(sys.argv[2],'a') as output:
		alldata=getDataOnDate(sys.argv[1])
		if alldata is not None and len(alldata)>0:
			for prod in alldata:
				output.write('\001'.join(prod))
				output.write('\n')
				output.flush()
