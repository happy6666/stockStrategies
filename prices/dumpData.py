#!/usr/bin/python
#Dump prices
import urllib2
import datetime
import time
import os
import json
import sys

SD='stockcode'
ZXJ='zxj'
ZDE='zde'
ZDF='zdf'
ZS='zs'
JK='jk'
ZGJ='zgj'
ZDJ='zdj'
JLR='jlr'
CJL='cjl'
CJE='cje'
HSL='hsl'

def getOrElse(d,c,e):
	res=[]
	if isinstance(c,list):
		for f in c:
			res.append(getOrElse(d,f,e))
		return res
	else:
		if d.has_key(c) and ('%s'%d[c]).strip()>0:
			raw=('%s'%d[c]).strip().encode('utf8')
			if c=='zdf' or c=='hsl':
				return '%s'%(float(raw[:-1])/100)
			elif c=='jlr' or c=='cje':
				return '%s'%(float(raw)*10000)
			else:
				return raw
		else:
			return e

if __name__=='__main__':
	os.chdir('/home/yiwen/stockStrategies/prices')
	code2name=dict([(x[0][2:],x[1].encode('utf8')) for x in [l.strip().decode('utf8','ignore').split('\t') for l in file('code2name').readlines()]])
	filename=datetime.datetime.today().strftime('%Y-%m-%d')
	output=file('output/n_'+filename,'w')
	for i in range(1,57):
		time.sleep(3)
		try:
			print "http://stat.10jqka.com.cn/q?id=qs_page&ld=browser&size=1366x768&nj=1&ref=http%3A%2F%2Fq.10jqka.com.cn%2Fstock%2F&url=http%3A%2F%2Fq.10jqka.com.cn%2Fstock%2Ffl%2F&cs=705x1789&ts="+str(int((time.time()+5)*1000))
			print 'http://q.10jqka.com.cn/interface/stock/fl/zdf/desc/%s/hsa/quote'%i
			sys.stdout.flush()
			h2=urllib2.urlopen("http://stat.10jqka.com.cn/q?id=qs_page&ld=browser&size=1366x768&nj=1&ref=http%3A%2F%2Fq.10jqka.com.cn%2Fstock%2F&url=http%3A%2F%2Fq.10jqka.com.cn%2Fstock%2Ffl%2F&cs=705x1789&ts="+str(int((time.time()+5)*1000)))
			h2.read()
			html=urllib2.urlopen('http://q.10jqka.com.cn/interface/stock/fl/zdf/desc/%s/hsa/quote'%i)
			resp=html.read()
			js=json.loads(resp)
			if js.has_key('data'):
				for line in js.get('data'):
					if code2name.has_key(line.get('stockcode')):
						output.write('%s\001%s\001%s\n'%('\001'.join(getOrElse(line,[SD,ZXJ,ZDF,ZDE,ZS,JK,ZGJ,ZDJ,JLR,CJL,CJE,HSL],'-99')),code2name[line.get('stockcode')],filename))
						output.flush()
			else:
				time.sleep(65)
				continue
		except IOError:
			time.sleep(65)
			continue
	output.close()
