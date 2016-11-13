#!/usr/bin/python
import urllib2
import os
import sys
import time
from bs4 import BeautifulSoup

os.chdir('/home/yiwen/stockStrategies/addition')

def getRawContent(code,s=0):
	t=60
	while True:
		try:
			response=urllib2.urlopen('http://stockpage.10jqka.com.cn/%s/bonus/#additionprofile'%(code.strip()[2:]))
			content=response.read()
			soup=BeautifulSoup(content)
			if soup.find('div',attrs={'class':'m_header'}) is not None:
				return soup
		except:
			pass
		time.sleep(t)
		t+=60

def getAdditionProfile(content):
	return content.find(attrs={'id':'additionprofile','class':'bd'})

def getConclusion(part):
	return ''.join([s.strip().encode('utf8','ignore') for s in part.div.get_text().splitlines()])

def parseUnit(s):
	if s.strip()=='--':
		return 'NULL'
	ssplits=s.strip().split(' ')
	if len(ssplits)>3:
		print 'Error:'+s.encode('utf8')
		#sys.exit(1)
		try:
			tmp=str(float(ssplits[0]))
			return tmp
		except:
			return 'NULL'
	if len(ssplits)==1:
		return "'"+s+"'"
	if len(ssplits)==2:
		if ssplits[1].find(u'\u4ebf')==0:
			return str(float(ssplits[0])*100000000)
		elif ssplits[1].find(u'\u4e07')==0:
			return str(float(ssplits[0])*10000)
		elif len(ssplits[1])==1:
			return str(ssplits[0])
		else:
			print 'Error:'+s.encode('utf8')
			sys.exit(1)
	if len(ssplits)==3:
		if ssplits[2].find(u'\u4ebf')==0:
			return str(float(ssplits[1])*100000000)
		elif ssplits[2].find(u'\u4e07')==0:
			return str(float(ssplits[1])*10000)
		elif len(ssplits[2])==1:
			return str(ssplits[1])
		else:
			print 'Error:'+s.encode('utf8')
			sys.exit(1)

def getFulltable(part):
	i=0
	data=[]
	for s in part.stripped_strings:
		if not s.strip()==u'\uff1a':
			i+=1
			if i%2==0:
				data.append(parseUnit(s))
	return data

if __name__=='__main__':
	if len(sys.argv)<2:
		print 'Usage:COMMAND <output>'
		sys.exit(1)

	if os.path.exists(sys.argv[1]):
		print '%s file exists'%sys.argv[1]
		sys.exit(1)

	input=file('todo.list')
	output=file(sys.argv[1],'w')
	data4write=[]
	while True:
		data=input.readline()
		if len(data)==0:
			break
		code=data.strip()[2:]
		print code
		sys.stdout.flush()
		time.sleep(3)
		soup=getRawContent(data)
		targetDiv=getAdditionProfile(soup)
		if targetDiv is not None:
			tables=targetDiv.find_all('table',recursive=False)
			for subtable in tables:
				results=getFulltable(subtable)
				try:
					data4write.append('('+str(code)+','+','.join(results).encode('utf8','ignore')+')')
				except:
					pass
	for i in range(0,len(data4write)):
		if i<(len(data4write)-1):
			output.write(data4write[i]+',\n')
		else:
			output.write(data4write[i]+';\n')
	output.close()
