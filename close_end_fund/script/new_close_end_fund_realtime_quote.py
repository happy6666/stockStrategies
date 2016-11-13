#!/usr/bin/python
import sys
import time
import tushare as ts
import json
from datetime import datetime

_START=datetime.strptime(datetime.strftime(datetime.now(),'%Y%m%d')+'092955','%Y%m%d%H%M%S')
_END=datetime.strptime(datetime.strftime(datetime.now(),'%Y%m%d')+'150005','%Y%m%d%H%M%S')

def read_codes(input):
    codes=[]
    for line in input:
        jobj=json.loads(line)
        codes.append(jobj['code'])
    return codes

if __name__=='__main__':
    if len(sys.argv)<3:
        print 'Usage:code_file output_file'
        sys.exit(1)
    with file(sys.argv[1]) as input:
        codes=read_codes(input)
    t=datetime.now()
    print 'START at %s'%datetime.strftime(t,'%Y%m%d_%H:%M:%S')
    with file(sys.argv[2],'a') as output:
        while True:
            t=datetime.now()
            #start from 9:29:55 to 15:0:05
            if t>=_START and t<=_END:
                #get realtime quote every 2.01 seconds
                df = ts.get_realtime_quotes(codes)
                xlines=df.shape[0]
                for i in xrange(xlines):
                    json.dump(df.iloc[i,:].to_json(),output)
                    output.write('\n')
                    output.flush()
                time.sleep(2.01)
            else:
                time.sleep(0.005)
                if t>_END:
                    print 'END at %s'%datetime.strftime(t,'%Y%m%d_%H:%M:%S')
                    break
