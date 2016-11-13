#!/bin/bash
DIR=/home/yiwen/stockStrategies/jupai
YESTERDAY=$(date --date='200 day ago' +'%Y%m%d')
cd $DIR
echo "
use quantum;
select a.p_date as 'date',concat('\"<tab>',a.code,'\"') code,a.name,b.curr_price as c_price,avg_price deal_price,'NULL' as 'volumn(wg)',amount 'amount(wy)',round(amount*avg_price/(c.value/10000)/b.curr_price,5) '1_ratio(deal*amount/(flowvalue*close))',a.obj_name from jupai a join prices b on a.code=b.code join flowvalue c on a.code=c.code where a.p_date >= str_to_date('${YESTERDAY}','%Y%m%d') and b.curr_price<avg_price and length(a.obj_name) >13 order by round(amount*avg_price/(c.value/10000)/b.curr_price,5) desc;
" > tmp.sql
mysql -uroot -proot < tmp.sql > tmp.txt
iconv -f utf-8 -t gb18030 tmp.txt > jupai.csv 
sed -i "s/\t/,/g" jupai.csv
sed -i "s/<tab>/\t/g" jupai.csv

echo "
use quantum;
select a.p_date as 'date',concat('\"<tab>',a.code,'\"') code,a.name,b.curr_price as c_price,avg_price deal_price,'NULL' as 'volumn(wg)',amount 'amount(wy)',round(amount*avg_price/(c.value/10000)/b.curr_price,5) '1_ratio(deal*amount/(flowvalue*close))',a.obj_name from jupai a join prices b on a.code=b.code join flowvalue c on c.code=a.code where a.p_date >= str_to_date('${YESTERDAY}','%Y%m%d') and b.curr_price<avg_price and length(a.obj_name) <= 13 order by round(amount*avg_price/(c.value/10000)/b.curr_price,5) desc;
" > tmp.sql
mysql -uroot -proot < tmp.sql > tmp_gs.txt
iconv -f utf-8 -t gb18030 tmp_gs.txt > jupai_gs.csv 
sed -i "s/\t/,/g" jupai_gs.csv
sed -i "s/<tab>/\t/g" jupai_gs.csv
sed -i "1d" jupai_gs.csv

echo "" >> jupai.csv
echo "" >> jupai.csv
echo "" >> jupai.csv
cat jupai_gs.csv >> jupai.csv
