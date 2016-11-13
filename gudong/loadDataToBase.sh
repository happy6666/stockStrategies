#!/bin/bash
DIR=/home/yiwen/stockStrategies/gudong
OUTPUT=gudong.dat
cd $DIR
python dumpData.py codes.list ${OUTPUT} 1> dump.log 2>&1
mv ${OUTPUT} /var/lib/mysql/quantum/${OUTPUT}
mysqlimport -uroot -proot quantum ${OUTPUT} -r --fields-terminated-by=
mv /var/lib/mysql/quantum/${OUTPUT} history/${OUTPUT}_$(date +'%Y%m%d')
