#Load history data
#!/bin/bash
DIR=/home/yiwen/stockStrategies/prices
YEAR=$(date --date='1 year ago' +'%Y')
YESTERDAY=$(date --date='0 days ago' +'%Y-%m-%d')
cd $DIR
OUTPUT=historydata.dat
python dumpHistoryPriceData.py codes.list ${OUTPUT} ${YEAR}
mv ${OUTPUT} /var/lib/mysql/quantum/price.dat
#mysqlimport -uroot -proot quantum price.dat -r --fields-terminated-by=
mv /var/lib/mysql/quantum/price.dat output/${OUTPUT}_${YESTERDAY}
