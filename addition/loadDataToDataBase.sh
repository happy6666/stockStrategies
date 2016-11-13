#!/bin/bash
YESTERDAY=$(date --date='0 days ago' +'%Y-%m-%d')
DIR=/home/yiwen/stockStrategies/addition
cd $DIR
python dumpDataFromURL.py additionprofile 1 >> job.log 2>>job.err
echo "truncate table quantum.addition;" > tmp.sql
echo "insert into quantum.addition values ">> tmp.sql
cat additionprofile >> tmp.sql
mysql -uroot -proot < tmp.sql
mv additionprofile history/additionprofile.${YESTERDAY}
