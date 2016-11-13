#!/bin/bash
DIR=/home/yiwen/stockStrategies/gudong
cd $DIR
echo "
use quantum;
select a.p_date date,concat('\"<tab>',a.code,'\"') as code,c.name,gudong from gudong a join (select code,max(p_date) mpdate from gudong group by code) b on (a.code=b.code and a.p_date=b.mpdate) join prices c on (a.code=c.code) where gudong like '%汇金%' or gudong like '%证券金融%' or gudong like '%社会保障基金%' or gudong like '%全国社保基金%' order by a.p_date desc,a.code,gudong;
" > tmp.sql
mysql -uroot -proot < tmp.sql > tmp.txt
iconv -f utf-8 -t gb18030 tmp.txt > gudong.csv 
sed -i 's/\t/,/g' gudong.csv 
sed -i 's/<tab>/\t/g' gudong.csv
