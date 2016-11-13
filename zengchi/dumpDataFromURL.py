#!/usr/bin/python
import os
import sys
import urllib2
import bs4
import time
import datetime
from bs4 import BeautifulSoup

def getRawData(output):
	url='http://data.10jqka.com.cn/financial/ggjy/field/enddate/order/desc/ajax/1/page/%s/'
	t=60
	page=1
	pageMax=1
	while True:
		try:
			time.sleep(3)
			turl=url%(page,)
			print turl
			sys.stdout.flush()
			response=urllib2.urlopen(turl)
			html=response.read()
			soup=BeautifulSoup(html,from_encoding='gb18030')
			if soup.body is not None:
				if page==1:
					span=soup.find('span',attrs={'class':'page_info'})
					if span is not None:
						span=''.join(span.stripped_strings)
						pageMax=int(span[span.rfind('/')+1:])
				result,keep=parseDate(soup)
				if result is not None:
					for l in result:
						output.write('\001'.join(l).encode('utf8','ignore')+'\n')
						output.flush()
				page+=1
				if page > pageMax or (not keep):
					break
				continue
			else:
				pass
		except:
			pass
		time.sleep(t)
		t+=60

def parseDate(soup):
	data=[]
	yesterday=(datetime.datetime.today()+datetime.timedelta(days=0)).strftime('%Y-%m-%d')
	finalstate=True
	for tr in soup.tbody.find_all('tr'):
		if type(tr) is bs4.element.Tag:
			line=[]
			for i,col in enumerate(tr.find_all('td')):
				if not i==0 and (not i==11):
					if i==5 or i==6 or i==8:
						if ''.join(col.stripped_strings).endswith(u'\u2030'):
							line.append(str(float((''.join(col.stripped_strings))[:-1])/1000))
						elif ''.join(col.stripped_strings).endswith(u'\u4e07'):
							line.append(str(float((''.join(col.stripped_strings))[:-1])*10000))
						else:
							try:
								num=float(''.join(col.stripped_strings))
								line.append(str(num))
							except:
								line.append('0')
								sys.stderr.write(''.join(col.stripped_strings))
								sys.stderr.flush()
								pass
					else:
						line.append(''.join(col.stripped_strings))
			if line[3] == yesterday:
				data.append(line)
			else:
				finalstate=False
				continue
	return (data,finalstate)

if __name__=='__main__':
	if len(sys.argv)<2:
		print 'Usage:COMMAND <output>'
		sys.exit(1)

	if os.path.exists(sys.argv[1]):
		print '%s file exists'%sys.argv[1]
		sys.exit(1)
	
	output=file(sys.argv[1],'w')
	getRawData(output)
	output.close()
