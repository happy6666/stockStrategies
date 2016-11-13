import bs4
import time
import urllib2
from bs4 import BeautifulSoup

class PageParser:
	def getGeneralInfo(self,soup):
		result=[]
		for tr in soup.tbody.children:
			if type(tr) is bs4.element.Tag:
				data=[]
				for i,td in enumerate(tr.find_all('td')):
					if i==1:
						data.append(td.attrs['code'])
					if i>=2 and i<=10 and (not i==3):
						for s in td.stripped_strings:
							if s.endswith(r'''%'''):
								s=float(s[:-1])*0.01
								s=str(s)
							data.append(s)
					if i==11:
						data.append(td.find_all('a')[1].attrs['href'])
				result.append(data)
		return result
	
	def getDetailedInfo(self,code,soup):
		result=[]
		for i,tr in enumerate(soup.tbody.find_all('tr')):
			#previous 6 lines are buyer
			if ''.join(tr.stripped_strings).find(u'\u673a\u6784\u4e13\u7528')>=0 or ''.join(tr.stripped_strings).find(u'\u4ea4\u6613\u5355\u5143')>=0 or ''.join(tr.stripped_strings).find(u'\u603b\u90e8')>=0:
				data=[code]
				if i<6:
					data.append('0')
				else:
					data.append('1')
				ll=0
				for s in tr.stripped_strings:
					ll+=1
				for j,s in enumerate(tr.stripped_strings):
					if (ll==8 and j>=2 and j<=7) or (ll>8 and j>=3 and j<=8):
						if s.endswith('%'):
							s=float(s[:-1])*0.01
							s=str(s)
						data.append(s)	
				for s in tr.stripped_strings:
					if s.find(u'\u673a\u6784\u4e13\u7528')>=0:
						data.append(u'\u673a\u6784\u4e13\u7528')
						break
					if s.find(u'\u4ea4\u6613\u5355\u5143')>=0:
						data.append(s)
						break
					if s.find(u'\u603b\u90e8')>=0:
						data.append(s)
						break
				result.append(data)
		return result

	def parseURL(self,url):
		wait=60
		soup=None
		while True:
			response=urllib2.urlopen(url)
			html=response.read()
			soup=BeautifulSoup(html,from_encoding='gb18030')
			if soup.tbody is not None:
				return soup	
			else:
				time.sleep(wait)
				wait+=65
			
