#!/bin/bash
DIR=/home/yiwen/stockStrategies/puofa
TODAY=$(date +'%Y-%m-%d')
cd $DIR
echo "
use quantum;
select concat('\"<tab>',code,'\"') code,name,c_price as 'c_price(fuquan)',faxing_price from (select a.code,a.name,a.price as c_price,b.price as faxing_price from (select * from fuquanprice where p_date='${TODAY}') a join puofa b on (a.code=b.code) ) tmp where faxing_price<=c_price and c_price!=0;
" > tmp.sql
mysql -uroot -proot < tmp.sql > tmp.txt
iconv -f utf-8 -t gb18030 tmp.txt > puofa.csv 
sed -i "s/\t/,/g" puofa.csv
sed -i "s/<tab>/\t/g" puofa.csv
