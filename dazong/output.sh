#!/bin/bash
DIR=/home/yiwen/stockStrategies/dazong
YESTERDAY=$(date --date='15 day ago' +'%Y%m%d')
TODAY=$(date +'%Y%m%d')
cd $DIR
echo "
use quantum;
select t1.p_date as 'date',concat('\"<tab>',t1.code,'\"') as code,t1.name,t2.curr_price as c_price,t1.deal_price,t1.count as 'volume(wg)',if(t1.deal_price*t1.count>1,round(t1.deal_price*t1.count,0),t1.deal_price*t1.count) as '3_amount(wy)',round(t2.curr_price/t1.deal_price,2) as '2_ratio(close/deal)',bct.bc bc15,sct.sc sc15,bct.bc-sct.sc 'diff15(bc-sc)',bcttd.bc bc,scttd.sc sc,bcttd.bc-scttd.sc 'diff(bc-sc)',round(t1.deal_price*t1.count*t1.deal_price/t2.curr_price/(t3.value/10000),5) as '1_deal*amount/(close*flowvalue)',buy_dealer,sold_dealer from 
(select * from dazong_general where str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and (buy_dealer='机构专用' or buy_dealer like '%交易单元%' or buy_dealer like '%总部%')) t1 join (select code,curr_price from prices) t2 on t1.code=t2.code join (select code,value from flowvalue) t3 on t1.code=t3.code
,(select t1.code,if(t2.code is null,0,c) bc from (select distinct code from dazong_general) t1 left outer join (select code,count(*) c from (select * from dazong_general where str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and (buy_dealer='机构专用' or buy_dealer like '%交易单元%' or buy_dealer like '%总部%')) tmp group by code) t2 on t1.code=t2.code) bct
,(select t1.code,if(t2.code is null,0,c) sc from (select distinct code from dazong_general) t1 left outer join (select code,count(*) c from (select * from dazong_general where str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and (sold_dealer='机构专用' or sold_dealer like '%交易单元%' or sold_dealer like '%总部%')) tmp group by code) t2 on t1.code=t2.code) sct
,(select t1.code,t1.p_date,if(t2.code is null,0,c) bc from (select distinct code,p_date from dazong_general) t1 left outer join (select code,p_date,count(*) c from (select * from dazong_general where (buy_dealer='机构专用' or buy_dealer like '%交易单元%' or buy_dealer like '%总部%')) tmp group by code,p_date) t2 on (t1.code=t2.code and t1.p_date=t2.p_date)) bcttd
,(select t1.code,t1.p_date,if(t2.code is null,0,c) sc from (select distinct code,p_date from dazong_general) t1 left outer join (select code,p_date,count(*) c from (select * from dazong_general where (sold_dealer='机构专用' or sold_dealer like '%交易单元%' or sold_dealer like '%总部%')) tmp group by code,p_date) t2 on (t1.code=t2.code and t1.p_date=t2.p_date)) scttd
where t1.code=bct.code and t1.code=sct.code and bct.code=sct.code and bcttd.code=scttd.code and bcttd.p_date=t1.p_date and scttd.p_date=t1.p_date and t1.code=bcttd.code and t1.code=scttd.code and bcttd.p_date=scttd.p_date
order by 15 desc,8,7 desc;
" > tmp.sql
mysql -uroot -proot < tmp.sql > tmp.txt 
iconv -f utf-8 -t gb18030 tmp.txt > dazong.csv
sed -i 's/\t/,/g' dazong.csv
sed -i 's/<tab>/\t/g' dazong.csv

echo "
use quantum;
select t1.p_date as 'date',concat('\"<tab>',t1.code,'\"') as code,t1.name,t2.curr_price as c_price,t1.deal_price,t1.count as 'volume(wg)',if(t1.deal_price*t1.count>1,round(t1.deal_price*t1.count,0),t1.deal_price*t1.count) as '3_amount(wy)',round(t2.curr_price/t1.deal_price,2) as '2_ratio(close/deal)',bct.bc bc15,sct.sc sc15,bct.bc-sct.sc 'diff15(bc-sc)',bcttd.bc bc,scttd.sc sc,bcttd.bc-scttd.sc 'diff(bc-sc)',round(t1.deal_price*t1.count*t1.deal_price/t2.curr_price/(t3.value/10000),2) as '1_deal*amount/(close*flowvalue)',buy_dealer ,sold_dealer from 
(select * from dazong_general where str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and ((buy_dealer!='机构专用' and buy_dealer not like '%交易单元%' and buy_dealer not like '%总部%') and (sold_dealer='机构专用' or sold_dealer like '%交易单元%' or sold_dealer like '%总部%'))) t1 join (select code,curr_price from prices) t2 on t1.code=t2.code join (select code,value from flowvalue) t3 on t1.code=t3.code
,(select t1.code,if(t2.code is null,0,c) bc from (select distinct code from dazong_general) t1 left outer join (select code,count(*) c from (select * from dazong_general where str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and (buy_dealer='机构专用' or buy_dealer like '%交易单元%' or buy_dealer like '%总部%')) tmp group by code) t2 on t1.code=t2.code) bct
,(select t1.code,if(t2.code is null,0,c) sc from (select distinct code from dazong_general) t1 left outer join (select code,count(*) c from (select * from dazong_general where str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and (sold_dealer='机构专用' or sold_dealer like '%交易单元%' or sold_dealer like '%总部%')) tmp group by code) t2 on t1.code=t2.code) sct
,(select t1.code,t1.p_date,if(t2.code is null,0,c) bc from (select distinct code,p_date from dazong_general) t1 left outer join (select code,p_date,count(*) c from (select * from dazong_general where (buy_dealer='机构专用' or buy_dealer like '%交易单元%' or buy_dealer like '%总部%')) tmp group by code,p_date) t2 on (t1.code=t2.code and t1.p_date=t2.p_date)) bcttd
,(select t1.code,t1.p_date,if(t2.code is null,0,c) sc from (select distinct code,p_date from dazong_general) t1 left outer join (select code,p_date,count(*) c from (select * from dazong_general where (sold_dealer='机构专用' or sold_dealer like '%交易单元%' or sold_dealer like '%总部%')) tmp group by code,p_date) t2 on (t1.code=t2.code and t1.p_date=t2.p_date)) scttd
where t1.code=bct.code and t1.code=sct.code and bct.code=sct.code and bcttd.code=scttd.code and t1.code=bcttd.code and t1.code=scttd.code and bcttd.p_date=t1.p_date and scttd.p_date=t1.p_date and bcttd.p_date=scttd.p_date
order by 15 desc,8,7 desc;
" > tmp.sql
mysql -uroot -proot < tmp.sql > tmp_so.txt 
iconv -f utf-8 -t gb18030 tmp_so.txt > dazong_so.csv
sed -i 's/\t/,/g' dazong_so.csv
sed -i 's/<tab>/\t/g' dazong_so.csv
sed -i '1d' dazong_so.csv
echo "" >> dazong.csv
echo "" >> dazong.csv
echo "" >> dazong.csv
cat dazong_so.csv >> dazong.csv
