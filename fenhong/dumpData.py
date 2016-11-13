import sys
import time
import urllib2
from bs4 import BeautifulSoup

def parseData(url):
	req=urllib2.urlopen(url)
	data=req.read()
	soup=BeautifulSoup(data,from_encoding='utf-8')
	target=soup.find(id='sharebonus_1')
	if target is None:
		return None
	tds=target.find('tbody').find_all('td')
	result=[]
	tmp=[]
	for i,td in enumerate(tds):
		if (i+1)%9!=0:
			tmp.append(td.get_text())
		else:
			tmp.append(td.get_text())
			if len(tmp)!=9:
				print '\001'.join(tmp).encode('utf8')
				print 'Error:%s'%url
			result.append(tmp[:-1])
			tmp=[]
	return result

if __name__=='__main__':
	fi=file(sys.argv[1])
	fo=file(sys.argv[2],'w')
	while True:
		line=fi.readline()
		if len(line)==0:
			break
		line=line.strip()
		print line
		sys.stdout.flush()
		t=60
		while True:
			res=parseData('http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/%s.phtml'%line)
			time.sleep(3)
			if not res is None:
				for row in res:
					fo.write(line+'\001'+'\001'.join(row).encode('utf8')+'\n')
				break
			else:
				t+=60
				time.sleep(t)
