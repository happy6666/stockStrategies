import urllib2
import time
import bs4
from bs4 import BeautifulSoup

class PageParser:

	def getInfo(self,soup):
		data=[]
		if soup.tbody is not None:
			for tr in soup.tbody.children:
				if type(tr) is bs4.element.Tag:
					line=[]
					for i,col in enumerate(tr.find_all('td')):
						if i>=1 and i<=9:
							s=''.join(col.stripped_strings)				
							if s.strip().endswith(r'%'):
								s=float(s[:-1])*0.01
								s=str(s)
							line.append(s)
					data.append(line)
		return data

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
