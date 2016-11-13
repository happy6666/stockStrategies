# coding: utf-8
import sys
from datetime import datetime
import time
import urllib2

TODAY=datetime.today().strftime('%Y%m%d')

def getData():
	url='http://www.cffex.com.cn/quote_FutureAll.txt?t=%s000'%(time.mktime(datetime.now().timetuple()))
	headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36','Host':'www.cffex.com.cn'}
	req=urllib2.Request(url,headers=headers)
	page=urllib2.urlopen(req,timeout=3)
	data=page.read()
	result=[]
	for i,line in enumerate(data.strip().split('\n')):
		if i>0:
			tmp=line.strip().split(',')
			tmp.append(time.strftime('%Y-%m-%d %H:%M:%S'))
			result.append(tmp)
	return result

if __name__=='__main__':
	data=getData()	
	if data is not None and len(data)>0:
		with file(sys.argv[1],'a') as output:
			for line in data:
				output.write('\001'.join(line))
				output.write('\n')
