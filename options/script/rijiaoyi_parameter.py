#!/usr/bin/python
# coding: utf-8
import sys
import urllib2
import json
import time
from datetime import datetime

SETTLEMENT='Settlement'
CR='COMMODITYDELIVERYFEERATION'
CU='COMMODITYDELIVERYFEEUNIT'
DR='DISCOUNTRATE'
IID='INSTRUMENTID'
LR='LONGMARGINRATIO'
SP='SETTLEMENTPRICE'
SR='SHORTMARGINRATIO'
SL='SPEC_LONGMARGINRATIO'
SS='SPEC_SHORTMARGINRATIO'
TR='TRADEFEERATION'
TU='TRADEFEEUNIT'
TD='TRADINGDAY'
UD='UPDATE_DATE'
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
            time.sleep(3)
            url=urllib2.urlopen('http://www.shfe.com.cn/data/instrument/Settlement%s.dat'%ts)
            data=url.read()
            js=json.loads(data,parse_float=None,parse_int=None)
            for ele in js[SETTLEMENT]:
                tmplist=_getOrElse(ele,[IID,TD,SP,TR,TU,CU,LR,SR,SL,SS,DR,UD],'None')
                tmplist.append(TODAY)
                alldata.append(tmplist)
            break
        except urllib2.HTTPError as e:
            print '%s->No data on date:%s'%(e.code,ts)
            break
        except Exception as e:
            print 'Error when get data on date:%s\n%s'%(ts,e)
            t+=60
            time.sleep(t)
    return alldata

if __name__=='__main__':
    with file(sys.argv[2],'a') as output:
        alldata=getDataOnDate(sys.argv[1])
        for prod in alldata:
            output.write('\001'.join(prod))
            output.write('\n')
