#!/bin/bash
DIR=/home/yiwen/stockStrategies/dazong
OUTPUT=dazong_general.dat
cd $DIR
python dumpDataFromURL.py ${OUTPUT}
mv ${OUTPUT} /var/lib/mysql/quantum/.
mysqlimport -uroot -proot quantum ${OUTPUT} -r --fields-terminated-by=
mv /var/lib/mysql/quantum/${OUTPUT} history/${OUTPUT}_$(date +'%Y%m%d')
