#!/usr/bin/python
# coding: utf-8
import sys
import time
import urllib2
from bs4 import BeautifulSoup

req='http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/%s/displaytype/30.phtml';
desired=set([u'\u622a\u81f3\u65e5\u671f','1','2','3','4','5','6','7','8','9','10'])

def parseData(code):
	global req
	url=req%code
	rep=urllib2.urlopen(url)
	t=3
	while True:
		time.sleep(t)
		data=rep.read()
		soup=BeautifulSoup(data,from_encoding='gb18030')
		if soup.find(id='Table1') is not None:
			break
		else:
			t+=60
	trs=soup.find(id='Table1').tbody.find_all('tr')
	final=[]
	res=[]
	for tr in trs:
		if tr.td.get_text()==u'\u622a\u81f3\u65e5\u671f':
			if len(res)>0:
				t=res[0]
				final.append('\n'.join([code+'\001'+l+'\001'+t for l in res[1:]]))
			res=[]
		if tr.td.get_text().strip() in desired and len(tr.find_all('td'))>1:
			res.append(tr.find_all('td')[1].get_text().strip())
	if len(res)>0:
		t=res[0]
		final.append('\n'.join([code+'\001'+l+'\001'+t for l in res[1:]]))
	return '\n'.join(final)

if __name__=='__main__':
	f=file(sys.argv[1])	
	output=file(sys.argv[2],'w') 
	while True:
		line=f.readline()
		if len(line)==0:
			break
		print line.strip()
		sys.stdout.flush()
		forout=parseData(line.strip()).encode('utf8')
		if len(forout)>0:
			output.write(forout+'\n')
			output.flush()
	output.close()
