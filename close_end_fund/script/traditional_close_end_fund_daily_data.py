#!/usr/bin/python
import sys
import requests
import json
from datetime import datetime
url='''http://fund.ijijin.cn/data/Net/fbs/ctx_rate_desc_0_0_1_9999_0_0_0_jsonp_g.html'''

def get_net_value(output):
	#get the response
	page=requests.get(url)
	#get the json part
	jobj=json.loads(page.content[2:-1])
	if jobj['error']['msg']=='is access':
		for k,v in jobj['data']['data'].iteritems():
			v['code0']=k
			v['c_date']=datetime.strftime(datetime.today(),'%Y%m%d %H:%M')
			json.dump(v,output)
			output.write('\n')
			output.flush()
	else:
		raise Exception

if __name__=='__main__':
	if len(sys.argv)<2:
		print 'Usage:output_file'
		sys.exit(1)
	with file(sys.argv[1],'a') as output:
		get_net_value(output)
