#!/usr/bin/python
import urllib2
import sys
from bs4 import BeautifulSoup
import time

def getData(code):
	url='http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/%s.phtml'%(code,)
	t=3
	target=None
	while True:
		time.sleep(t)
		rep=urllib2.urlopen(url)
		data=rep.read()
		soup=BeautifulSoup(data,from_encoding='gb18030')
		target=soup.find(id='comInfo1')
		if target is not None:
			break
		else:
			t+=60
			time.sleep(t)
			continue
	try:
		res=float(target.find_all('tr')[3].find_all('td')[1].get_text())
		return res
	except:
		print 'Error:'+code+'->'+target.find_all('tr')[3].find_all('td')[1].get_text()
		return None

if __name__=='__main__':
	f=file(sys.argv[1])
	output=file(sys.argv[2],'w')
	while True:
		line=f.readline()
		if len(line)==0:
			break
		line=line.strip()
		print line
		sys.stdout.flush()
		val=getData(line)
		if val is not None:
			output.write(line+'\001'+str(val)+'\n')	
			output.flush()
	output.close()
