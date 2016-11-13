#!/usr/bin/python
import urllib2 as ub
import time as ts
import traceback as tb
import sys
import xml.etree.ElementTree as xmlParser

keys=['name','openprice','highprice','lowprice','newprice','risefall','buyprice','buyqty','sellprice','sellqty','matchqty','openinterest','closeprice','clearprice','lastcloseprice','lastclearprice']

def getRawData():
	req=ub.Request('http://quote.dce.com.cn/data/quoteAll.xml')
	req.add_header('user-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)')
	res=[]
	try:
		url=ub.urlopen(req,timeout=5)
		data=url.read()
		xmlData=xmlParser.fromstring(data)
		for prod in xmlData.findall('product'):
			for cont in prod.findall('contract'):
				tmp=[]
				for k in keys:
					tmp.append(cont.get(k,'-'))
				res.append(tmp)
		return res
	except AttributeError,e:
		print tb.format_exc()
	except Exception,e:
		print tb.format_exc()

if __name__=='__main__':
	with file(sys.argv[1],'a') as output:
		data=getRawData()
		for line in data:
			output.write('\001'.join(line)+'\001'+ts.strftime('%Y-%m-%d %H:%M:%S')+'\n')
