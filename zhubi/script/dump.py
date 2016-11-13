#!/usr/bin/python
import urllib2
import sys
import time
import socket

maxRetry=1

def dump(code,dstr):
	if str(code).startswith('6'):
		code=('sh%s'%code).strip()
	else:
		code=('sz%s'%code).strip()
	t=0
	retry=0
	while True:
		try:
			req=urllib2.Request('http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s'%(dstr,code))
			req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
			resp=urllib2.urlopen(req,timeout=3)
			content=resp.read()
			output=file('/home/yiwen/stockStrategies/zhubi/rawdata/%s_%s'%(code.strip(),dstr.strip()),'w')
			output.write(content.decode('gb18030').encode('utf8'))
			output.close()
			t=t+3
			time.sleep(t)
			break
		except urllib2.HTTPError,e:
			if str(e).find('404')>0:
				print '404'
				break
			print e
			retry+=1
			if retry>maxRetry:
				break
			t=t+60
			time.sleep(t)

if __name__=='__main__':
	dump(sys.argv[1],sys.argv[2])
