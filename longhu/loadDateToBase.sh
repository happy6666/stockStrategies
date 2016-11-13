#!/bin/bash
DIR=/home/yiwen/stockStrategies/longhu
OUTPUT1=longhu_general.dat
OUTPUT2=longhu_detail.dat
YESTERDAY=$(date --date='0 days ago' +'%Y-%m-%d')
cd $DIR
python dumpLonghuData.py $OUTPUT1 $OUTPUT2 $YESTERDAY 1
mv ${OUTPUT1} /var/lib/mysql/quantum/.
mv ${OUTPUT2} /var/lib/mysql/quantum/.
mysqlimport -uroot -proot quantum ${OUTPUT1} -r --fields-terminated-by=
mysqlimport -uroot -proot quantum ${OUTPUT2} -r --fields-terminated-by=
mv /var/lib/mysql/quantum/${OUTPUT1} history/${OUTPUT1}_$(date +'%Y%m%d')
mv /var/lib/mysql/quantum/${OUTPUT2} history/${OUTPUT2}_$(date +'%Y%m%d')
