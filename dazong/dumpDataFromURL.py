#!/usr/bin/python
import os
import sys
import time
sys.path.append('.')
import parser
import datetime

def dumpDataFromUrl(url,out):
	yesterday=(datetime.datetime.today()+datetime.timedelta(days=0)).strftime('%Y-%m-%d')
	print yesterday
	pparser=parser.PageParser()
	page=1
	pageMax=1
	while True:
		cUrl=url%(page,)
		print cUrl
		sys.stdout.flush()
		time.sleep(3)
		soup=pparser.parseURL(cUrl)
		if page==1:
			pageMax=soup.find(attrs={'class':'m-page J-ajax-page'})
			if pageMax is not None:
				pageMax=pageMax.span.string
				pageMax=int(pageMax[pageMax.rfind('/')+1:])
		data=pparser.getInfo(soup)
		for line in data:
			if not line[0]==yesterday:
				if pageMax is not None:
					page=pageMax
				continue
			out.write('\001'.join(line[1:]).encode('utf8','ignore')+'\001'+line[0].encode('utf8','ignore')+'\n')
		out.flush()
		page+=1
		if page>pageMax:
			break

if __name__=='__main__':
	url='http://data.10jqka.com.cn/market/dzjy/field/enddate/order/desc/ajax/1/page/%s'
	if len(sys.argv)<2:
		print 'Usage:COMMAND <out>'
		sys.exit(1)

	if os.path.exists(sys.argv[1]):
		print '%s file exists'%(sys.argv[1],)
		sys.exit(1)

	out=file(sys.argv[1],'w')	
	dumpDataFromUrl(url,out)
