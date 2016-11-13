#!/bin/bash
DIR=/home/yiwen/stockStrategies/prices
YESTERDAY=$(date --date='0 days ago' +'%Y-%m-%d')
cd $DIR
python dumpData.py 
cp output/n_${YESTERDAY} /var/lib/mysql/quantum/price.dat
mv output/n_${YESTERDAY} /var/lib/mysql/quantum/prices.dat
mysqlimport -uroot -proot quantum price.dat -r --fields-terminated-by=
mysqlimport -d -uroot -proot quantum prices.dat -r --fields-terminated-by=
mv /var/lib/mysql/quantum/price.dat output/n_${YESTERDAY}
rm /var/lib/mysql/quantum/prices.dat
