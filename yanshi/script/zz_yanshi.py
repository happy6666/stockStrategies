#!/usr/bin/python
import urllib2 as ub
import time as ts
import traceback as tb
import sys
from bs4 import BeautifulSoup

def getRawData(dateStr):
	req=ub.Request('http://www.czce.com.cn/portal/exchange/%s/quotation/%s.htm'%(dateStr[0:4],dateStr))
	req.add_header('user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
	res=[]
	try:
		url=ub.urlopen(req,timeout=5)
		data=url.read()
		soup=BeautifulSoup(data,from_encoding='gb18030')
		allRows=soup.find('body').find('table').find('table').find_all('tr')
		for i,row in enumerate(allRows):
			if i!=0:
				tmp=[col.text.replace(',','') for col in row.find_all('td')]
				if tmp[0]!=u'\u5c0f\u8ba1' and tmp[0]!=u'\u603b\u8ba1':
					res.append(tmp)
		return res
	except ub.HTTPError,e:
		print tb.format_exc()
	except AttributeError,e:
		print tb.format_exc()
	except Exception,e:
		print tb.format_exc()
	return res


if __name__=='__main__':
	with file(sys.argv[2],'a') as input:
		res=getRawData(sys.argv[1])
		for l in res:
			input.write('\001'.join(l).encode('utf8')+'\001'+ts.strftime('%Y-%m-%d %H:%M:%S')+'\n')
