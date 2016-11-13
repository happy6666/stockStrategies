#!/usr/bin/python
#Dump flow value
import urllib2
import os
import sys
import json
import datetime
import time

if __name__=='__main__':
	URL='''http://d.10jqka.com.cn/v2/realhead/hs_%s/last.js'''
	fi=file(sys.argv[1])
	output=file(sys.argv[2],'w')
	p_date=datetime.datetime.today().strftime('%Y-%m-%d')
	while True:
		code=fi.readline()
		if len(code)==0:
			break
		code=code.strip()
		t=60
		c=True
		while c:
			time.sleep(3)
			http=urllib2.urlopen(URL%code)
			try:
				data=http.read()
				print code
				jobj=json.loads(data[data.find('{'):data.rfind('}')+1])
				if jobj.has_key('items') and jobj['items'].has_key('3475914'):
					if len(jobj['items']['3475914'])>0:
						output.write(code+'\001'+jobj['items']['3475914']+'\001'+p_date+'\n')	
						output.flush()
					c=False
				else:
					time.sleep(t)	
					t+=60
			except ValueError:
				pass
	output.close()
