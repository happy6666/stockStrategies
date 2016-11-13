#!/usr/bin/python
import urllib2 as ub
import time as ts
import traceback as tb
import sys
from bs4 import BeautifulSoup

def getRawData():
	req=ub.Request('http://www.shfe.com.cn/statements/delaymarket_all.html?isAjax=true')
	req.add_header('user-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
	res=[]
	try:
		url=ub.urlopen(req,timeout=5)
		data=url.read()
		soup=BeautifulSoup(data)
		rows=soup.find('table').find_all('tr')
		for i,r in enumerate(rows):
			if i>1:
				res.append([col.text.replace(',','') for col in r.find_all('td') ])
	except AttributeError,e:
		print tb.format_exc()
	except ub.HTTPError,e:
		print tb.format_exc()
	except Exception,e:
		print tb.format_exc()
	return res

if __name__=='__main__':
	with file(sys.argv[1],'a') as input:
		res=getRawData()
		for l in res:
			input.write('\001'.join(l).encode('utf8')+'\001'+ts.strftime('%Y-%m-%d %H:%M:%S')+'\n')
