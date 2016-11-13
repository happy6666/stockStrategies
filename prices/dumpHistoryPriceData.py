#!/usr/bin/python
import urllib2
import time
import sys
import json
import datetime as dt

start=2015
end=2016
code2name=dict([(x[0][2:],x[1]) for x in [l.strip().split('\t') for l in file('code2name').readlines()]])

def parseData(code,year):
	res=[]
	t=3
	time.sleep(t)
	url='http://d.10jqka.com.cn/v2/line/hs_%s/01/%s.js'%(code,year)
	print url
	sys.stdout.flush()
	while True:
		req=None
		try:
			req=urllib2.urlopen(url,timeout=3.5)
			break
		except urllib2.URLError,e:
			if str(e).find('404')>0:
				return None
			t+=60
			time.sleep(t)
			pass
		except:
			t+=60
			time.sleep(t)
			pass
	reqcode=req.getcode()
	if str(reqcode)=='200':
		data=req.read()
		if data.find('data')>0:
			js=json.loads(data[data.find('{'):data.rfind('}')+1])
			for day in js['data'].strip().split(';'):
				cols=day.strip().split(',')
				timestamp=dt.datetime.strptime(cols[0],'%Y%m%d').strftime('%Y-%m-%d')
				c_price=cols[4]
				if len(str(c_price))>0:
					res.append('\001'.join((str(code),code2name[code],str(c_price),timestamp)))
		else:
			print 'Error:',code
			print 'Data:',data
	else:
		res=None
	return res

if __name__=='__main__':
	codes=file(sys.argv[1])
	output=file(sys.argv[2],'w')
	if len(sys.argv)<4:
		start=1899
	else:
		start=int(sys.argv[3])
	while True:
		line=codes.readline()	
		if len(line)==0:
			break
		print line.strip()
		sys.stdout.flush()
		for year in range(end,start,-1):
			res=parseData(line.strip(),year)
			if res is not None and len(res)>0:
				output.write('\n'.join(res)+'\n')
				output.flush()
			else:
				break
	output.close()
