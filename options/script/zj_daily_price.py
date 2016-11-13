#!/usr/bin/python
# coding: utf-8
from bs4 import BeautifulSoup
import urllib2
import time
from datetime import datetime
import sys

TODAY=datetime.today().strftime('%Y%m%d')

def getDataOnDate(dateStr):
	url='http://www.cffex.com.cn/fzjy/mrhq/%s/%s/index.xml'%(dateStr[:-2],dateStr[-2:])
	headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36','X-Requested-With':'XMLHttpRequest'}
	req=urllib2.Request(url,headers=headers)
	page=urllib2.urlopen(req,timeout=5)
	data=page.read()
	soup=BeautifulSoup(data)
	dailyData=soup.findAll('dailydata')
	result=[]
	for i in xrange(len(dailyData)):
		lineRes=[]
		for j,res in enumerate(dailyData[i].strings):
			if j==0 and j=='':
				continue
			tmp=res.strip().replace('\s','').replace(',','')
			if len(tmp)>0:
				lineRes.append(str(tmp))
		if len(lineRes)>0:
			lineRes.append(TODAY)
			result.append(lineRes)
	if len(result)>0:
		return result
	else:
		return None

if __name__=='__main__':
	data=getDataOnDate(sys.argv[1])	
	if data is not None:
		with file(sys.argv[2],'a') as output:
			for line in data:
				output.write('\001'.join(line))
				output.write('\n')
