#!/usr/bin/python
import urllib2
import sys
import os
import bs4
from bs4 import BeautifulSoup
import datetime
import time

def getRawData(url):
	t=60
	while True:
		print url
		sys.stdout.flush()
		response=urllib2.urlopen(url)
		html=response.read()
		soup=BeautifulSoup(html,from_encoding='gb18030')
		if soup.tbody is not None:
			return soup
		else:
			time.sleep(t)
			t+=60

def parseData(output):
	page=1
	pageMax=1
	yesterday=(datetime.datetime.today()+datetime.timedelta(days=0)).strftime('%Y-%m-%d')
	print yesterday
	while True:
		url='http://data.10jqka.com.cn/financial/xzjp/field/DECLAREDATE/order/desc/ajax/1/page/%s/'%page
		time.sleep(3)
		soup=getRawData(url)
		for tr in soup.tbody.find_all('tr'):
			if type(tr) is bs4.element.Tag:
				data=[]
				for i,col in enumerate(tr.find_all('td')):
					if not i==0 and (not i==12):
						data.append(''.join(col.stripped_strings))
				if data[0]!=yesterday:
					page=pageMax
					break
				try:
					if data[6].endswith(u'\u4e07'):
						data[6]=str(float(data[6][0:-1]))
					if data[6].endswith(u'\u4ebf'):
						data[6]=str(float(data[6][0:-1])*10000)
					if data[9].endswith(u'\u4e07'):
						data[9]=str(float(data[9][0:-1]))
					if data[9].endswith(u'\u4ebf'):
						data[9]=str(float(data[9][0:-1])*10000)
					output.write(('\001'.join(data[1:])).encode('utf8','ignore')+'\001'+data[0].encode('utf8','ignore')+'\n')
					output.flush()
				except:
					print 'ERROR:'+'\001'.join(data[1:]).encode('utf8','ignore')+'\001'+data[0].encode('utf8','ignore')
					pass
		if page==1:
			pp=''.join(soup.find('span',attrs={'class':'page_info'}).stripped_strings)
			pageMax=int(pp[pp.rfind('/')+1:])
		page+=1
		if page > pageMax:
			break
	output.close()

if __name__=='__main__':
	if len(sys.argv)<2:
		print 'Usage:COMMAND <output>'
		sys.exit(1)
	
	if os.path.exists(sys.argv[1]):
		print '%s file exist'%sys.argv[1]
		sys.exit(1)

	output=file(sys.argv[1],'w')
	parseData(output)
