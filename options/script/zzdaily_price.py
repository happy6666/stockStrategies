#!/usr/bin/python
# coding: utf-8
import sys
import urllib2
import time
from datetime import datetime
from bs4 import BeautifulSoup

TODAY=datetime.today().strftime('%Y%m%d')
IMPORTANT='20151008'

def getDataOnDate(ts):
	t=0;
	alldata=[]
	while True:
		time.sleep(1)
		try:
			if ts>=IMPORTANT:
				req=urllib2.Request('http://www.czce.com.cn/portal/DFSStaticFiles/Future/%s/%s/FutureDataDaily.htm'%(ts[:4],ts))
				req.add_header('user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
				url=urllib2.urlopen(req,timeout=5)
			else:
				req=urllib2.Request('http://www.czce.com.cn/portal/exchange/%s/datadaily/%s.htm'%(ts[:4],ts))
				req.add_header('user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
				url=urllib2.urlopen(req,timeout=5)
			data=url.read()
			soup=BeautifulSoup(data,from_encoding='utf-8')
			if ts>=IMPORTANT:
				page=soup.find('table').find('table').find_all('tr')
			else:
				page=soup.find_all('table')[3].find_all('tr')
			for i,prod in enumerate(page):
				#skip first name line
				if i>0:
					tmplist=[('%s'%(col.text)).encode('utf8').replace(',','') for col in prod.find_all('td') if len(col.text.strip())>0]
					if tmplist[0].decode('utf8')==u'\u5c0f\u8ba1' or tmplist[0].decode('utf8')==u'\u603b\u8ba1':
						continue
					if len(tmplist)<13:
						tmplist.append('None')
						tmplist.append('None')
						tmplist.append('None')
					if not len(tmplist)==13:
						print 'Error on date:%s'%ts
						continue
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
