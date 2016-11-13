import sys
import time
import datetime
import urllib2
import datetime
from bs4 import BeautifulSoup

def getGuShu(code,date):
	url='http://vip.stock.finance.sina.com.cn/corp/view/vISSUE_ShareBonusDetail.php?stockid=%s&type=2&end_date=%s'%(code,date)
	print url
	sys.stdout.flush()
	t=3
	while True:
		time.sleep(t)
		try:
			req=urllib2.urlopen(url)
		except urllib2.URLError:
			t+=60
			continue
		data=req.read()
		soup=BeautifulSoup(data,from_encoding='utf-8')
		tbody=soup.find(id='sharebonusdetail')
		if tbody is None:
			t+=60
			continue
		else:
			return (tbody.find_all('tr')[23].find_all('td')[1].get_text().replace(',',''),tbody.find_all('tr')[24].find_all('td')[1].get_text().replace(',',''),tbody.find_all('tr')[25].find_all('td')[1].get_text().replace(',',''))

def parseData(url,code):
	req=None
	try:
		req=urllib2.urlopen(url)
	except:
		return None
	data=req.read()
	soup=BeautifulSoup(data,from_encoding='utf-8')
	target=soup.find(id='sharebonus_2')
	if target is None:
		return None
	tds=target.find('tbody').find_all('td')
	result=[]
	tmp=[]
	for i,td in enumerate(tds):
		if (i+1)%11!=0:
			if len(td.get_text())>0:
				tmp.append(td.get_text())
			else:
				tmp.append(' ')
		else:
			if len(td.get_text())>0:
				tmp.append(td.get_text())
				if tmp[0]!='--':
					gushu=getGuShu(code,tmp[0])
				else:
					tmp=[]
					continue
			else:
				tmp.append(' ')
			if len(tmp)!=11:
				print '\001'.join(tmp).encode('utf8')
				print 'Error:%s'%url
			else:
				tmp=tmp[:-2]
				if str(gushu[0])!='--':
					tmp.append(str(gushu[0]))
				else:
					tmp.append(str(-1))
				if str(gushu[1])!='--':
					tmp.append(str(gushu[1]))
				else:
					tmp.append(str(-1))
				if str(gushu[2])!='--':
					tmp.append(str(gushu[2]))
				else:
					tmp.append(str(-1))
				result.append(tmp)
			tmp=[]
	return result

if __name__=='__main__':
	fi=file(sys.argv[1])
	fo=file(sys.argv[2],'w')
	p_date=datetime.datetime.strftime(datetime.datetime.today(),'%Y-%m-%d')
	while True:
		line=fi.readline()
		if len(line)==0:
			break
		line=line.strip()
		print line
		sys.stdout.flush()
		t=60
		while True:
			res=parseData('http://vip.stock.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/%s.phtml'%line,line)
			time.sleep(3)
			if not res is None:
				for row in res:
					fo.write(line+'\001'+'\001'.join(row).encode('utf8')+'\001'+p_date+'\n')
					fo.flush()
				break
			else:
				t+=60
				time.sleep(t)
	fo.close()
