#!/bin/bash
DIR=/home/yiwen/stockStrategies/fenhong
OUTPUT=fenhong.dat
cd $DIR
python dumpData.py codes.list $OUTPUT
mv ${OUTPUT} /var/lib/mysql/quantum/.
mysqlimport -uroot -proot quantum ${OUTPUT} -r --fields-terminated-by=
mv /var/lib/mysql/quantum/${OUTPUT} history/${OUTPUT}_$(date +'%Y%m%d')
