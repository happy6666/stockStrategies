#!/usr/bin/python
# coding: utf-8
import sys
import urllib2
import json
import time
import traceback
from datetime import datetime

CURSOR='o_cursor'
RD='report_date'
UD='update_date'
CU='COMMODITYDELIVFEEUNIT'
HL='HEDGLONGMARGINRATIO'
HS='HEDGSHORTMARGINRATIO'
IID='INSTRUMENTID'
SP='SETTLEMENTPRICE'
SL='SPECLONGMARGINRATIO'
SS='SPECSHORTMARGINRATIO'
TR='TRADEFEERATIO'
TU='TRADEFEEUNIT'
TODAY=datetime.today().strftime('%Y%m%d')

def _getOrElse(d,k,e):
	res=[]
	if not isinstance(k,list):
		if d.has_key(k) and len(('%s'%d[k]).strip())>0:
			return ('%s'%d[k]).strip().encode('utf8')
		else:
			return e
	else:
		for key in k:
			res.append(_getOrElse(d,key,e))
		return res

def getDataOnDate(ts):
	alldata=[]
	t=0
	while True:
		try:
			time.sleep(1)
			req=urllib2.Request('http://www.shfe.com.cn/data/dailydata/js/js%s.dat'%ts)
			req.add_header('user-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
			url=urllib2.urlopen(req,timeout=5)
			data=url.read()
			js=json.loads(data,parse_float=None,parse_int=None)
			for ele in js[CURSOR]:
				tmplist=_getOrElse(ele,[IID,SP,TR,TU,CU,HL,HS,SL,SS],'None')
				tmplist.append(ts)
				if js.has_key(RD):
					tmplist.append(js[RD])
				else:
					tmplist.append(ts)
				if js.has_key(UD):
					tmplist.append(js[UD])
				else:
					tmplist.append(ts)
				tmplist.append(TODAY)
				alldata.append(tmplist)
			break
		except urllib2.HTTPError as e:
			print '%s->No data on date:%s'%(e.code,ts)
			break
		except Exception as e:
			print 'Error when get data on date:%s\n%s'%(ts,e)
			t+=60
			if t>70:
				break
			time.sleep(t)
	return alldata

if __name__=='__main__':
	with file(sys.argv[2],'a') as output:
		alldata=getDataOnDate(sys.argv[1])
		for prod in alldata:
			output.write('\001'.join(prod))
			output.write('\n')
