#!/bin/bash
DIR=/home/yiwen/stockStrategies/prices
YESTERDAY=$(date --date='0 days ago' +'%Y-%m-%d')
cd $DIR
python dumpData2.py codes.list flowvalue.dat
mv flowvalue.dat /var/lib/mysql/quantum/flowvalue.dat
mysqlimport -uroot -proot quantum flowvalue.dat -r --fields-terminated-by=
mv /var/lib/mysql/quantum/flowvalue.dat output/flowvalue.dat_${YESTERDAY}
