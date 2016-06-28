#!/usr/bin/python
# coding: utf-8
import sys
import urllib2
import json
import time as ts
from datetime import datetime

DAILY_TRADE_ARGUMENT='ContractDailyTradeArgument'
HL='HDEGE_LONGMARGINRATIO'
HS='HDEGE_SHORTMARGINRATIO'
IID='INSTRUMENTID'
LV='LOWER_VALUE'
SL='SPEC_LONGMARGINRATIO'
SS='SPEC_SHORTMARGINRATIO'
TD='TRADINGDAY'
UD='UPDATE_DATE'
UV='UPPER_VALUE'
TODAY=datetime.today().strftime('%Y%m%d')

def getOrElse(d,k,e):
	res=[]
	if not isinstance(k, list):
		if d.has_key(k) and len(d[k].strip())>0:
			return str(d[k].strip())
		else:
			return str(e)
	else:
		for key in k:
			res.append(getOrElse(d,key,e))
		return res

def getDataOnDate(time):
	alldata=[]
	t=0
	while True:
		ts.sleep(3)
		try:
			url=urllib2.urlopen('http://www.shfe.com.cn/data/instrument/ContractDailyTradeArgument%s.dat'%time)
			data=url.read()
			js=json.loads(data)
			if js.has_key(DAILY_TRADE_ARGUMENT):
				for ele in js[DAILY_TRADE_ARGUMENT]:
					tmplist=getOrElse(ele,[IID,TD,HL,HS,SL,SS,LV,UV,UD],'None')
					tmplist.append(TODAY)
					alldata.append(tmplist)
			else:
				'No DAILY_TRADE_ARGUMENT on date:%s'%(time)
			break
		except urllib2.HTTPError,e:
			print '%s->No data on date:%s'%(e.code,time)
			break
		except Exception,e:
			print 'Other error on date:%s\n%s'%(time,e)
			t+=60
			ts.sleep(t)
	return alldata

if __name__=='__main__':
	with file(sys.argv[2],'a') as output:
		alldata=getDataOnDate(sys.argv[1])
		for instru in alldata:
			output.write('\001'.join(instru))
			output.write('\n')
		output.close()
