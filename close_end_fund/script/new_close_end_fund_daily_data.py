#!/usr/bin/python
import requests
import time
from datetime import datetime
import sys
import json

url='''http://fund.ijijin.cn/data/Net/fbs/cxx_rate_desc_0_0_1_9999_0_0_0_jsonp_g.html'''
time=datetime.strftime(datetime.today(),'%Y%m%d %H:%M')

def get_data(output):
    page=requests.get(url)
    #get json part
    jobj=json.loads(page.content[2:-1])
    if jobj['error']['msg']=='is access':
        for k,v in jobj['data']['data'].iteritems():
            v['code0']=k
            v['c_time']=time
            json.dump(v,output)
            output.write('\n')
            output.flush()
    else:
        raise Exception

if __name__=='__main__':
    if len(sys.argv) < 2:
        print 'Usage:output_file'
        sys.exit(1)
    with file(sys.argv[1],'a') as output:
        get_data(output)

