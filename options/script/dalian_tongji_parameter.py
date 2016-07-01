#!/usr/bin/python
# coding: utf-8
import sys
import urllib2
import time
from datetime import datetime
from bs4 import BeautifulSoup

TODAY=datetime.today().strftime('%Y%m%d')

def getDataOnDate(ts):
    t=0;
    alldata=[]
    while True:
        time.sleep(3)
        try:
            url=urllib2.urlopen('http://www.dce.com.cn/PublicWeb/MainServlet?action=Pu00011_result&Pu00011_Input.trade_date=%s&Pu00011_Input.variety=all&Pu00011_Input.trade_type=0'%ts)
            data=url.read()
            soup=BeautifulSoup(data,from_encoding='utf-8')
            for i,prod in enumerate(soup.find('table').find('table').find_all('tr')):
                #skip first name line
                if i>0:
                    tmplist=[('%s'%(col.text.replace(',','').strip())).encode('utf8') for col in prod.find_all('td')]
                    tmplist.append(ts)
                    tmplist.append(TODAY)
                    #skip conclusion line
                    if len(tmplist[1])==0 and len(tmplist[2])==0 and len(tmplist[3])==0:
                        continue
                    alldata.append(tmplist)
            return alldata
        except urllib2.HTTPError as e:
            print '%s->Data not exist on date:%s'%(e.code,ts)
            return None
        except Exception as e:
            print 'Error on date:%s\n%s'%(ts,e)
            t+=60
            time.sleep(t)

if __name__=='__main__':
    with file(sys.argv[2],'a') as output:
        alldata=getDataOnDate(sys.argv[1])
        if alldata is not None and len(alldata)>0:
            for prod in alldata:
                output.write('\001'.join(prod))
                output.write('\n')
                output.flush()
