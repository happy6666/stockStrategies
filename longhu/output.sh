#!/bin/bash
DIR=/home/yiwen/stockStrategies/longhu
YESTERDAY=$(date --date='15 day ago' +'%Y%m%d')
TODAY=$(date --date='1 days ago' +'%Y%m%d')
cd $DIR
echo "
use quantum;
select tmp.p_date as 'date',concat('\"<tab>',tmp.code,'\"') code,t2.name,t3.curr_price c_price,'NULL' deal_price,'NULL' as 'volume1(wg)','NULL' as 'amount15(wy)','NULL' as 'ratio(close/deal)',bc bc15,sc sc15,diff15 'diff15(bc15-sc15)',if(bc1 is null,0,bc1) bc,if(sc1 is null,0,sc1) sc,if(diff1 is null,0,diff1) as '1_diff(bc-sc)',if(buy_amount>1,round(buy_amount,0),buy_amount) as 'buy_amount15(wy)',if(sold_amount>1,round(sold_amount,0),sold_amount) as 'sold_amount15(wy)',if(abs(buy_amount-sold_amount)>1,round(buy_amount-sold_amount,0),buy_amount-sold_amount) as 'net_amount15(wy)(buy_amount15-sold_amount15)',if(buy_amount1 is null,0,round(buy_amount1,0)) as 'buy_amount(wy)',if(sold_amount1 is null,0,round(sold_amount1,0)) as 'sold_amount(wy)',if(buy_amount1 is null,0,if(abs(buy_amount1-sold_amount1)>1,round(buy_amount1-sold_amount1,0),buy_amount1-sold_amount1)) as 'net_amount(wy)(buy_amount-sold_amount)',if(net_jigou is null,0,if(abs(net_jigou) > 1 ,round(net_jigou,0),net_jigou)) net_jigou15,if(net_jiaoyidanyuan is null,0,if(abs(net_jiaoyidanyuan)>1,round(net_jiaoyidanyuan,0),net_jiaoyidanyuan)) net_jiaoyidanyuan15,if(net_zongbu is null,0,if(abs(net_zongbu)>1,round(net_zongbu,0),net_zongbu)) net_zongbu15,concat('\"',reason,'\"') as reason from 
(select tmp1.code,bc,sc,bc-sc diff15,tmp1td.buy_amount+tmp2td.buy_amount buy_amount1,tmp1td.sold_amount+tmp2td.sold_amount sold_amount1,bctd bc1,sctd sc1,bctd-sctd diff1,tmp1.p_date,tmp1.buy_amount+tmp2.buy_amount as buy_amount,tmp1.sold_amount+tmp2.sold_amount as sold_amount,tmp3.buy_amount+tmp4.buy_amount-tmp3.sold_amount-tmp4.sold_amount as 'net_jigou',tmp5.buy_amount+tmp6.buy_amount-tmp5.sold_amount-tmp6.sold_amount as 'net_jiaoyidanyuan',tmp7.buy_amount+tmp8.buy_amount-tmp7.sold_amount-tmp8.sold_amount as 'net_zongbu' from 
		(select code,flag,count(*) bc,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,max(p_date) p_date from longhu_detail where flag='0' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date group by code,flag) tmp1 join
		(select code,flag,count(*) sc,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,max(p_date) p_date from longhu_detail where flag='1' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date group by code,flag) tmp2 on (tmp1.code=tmp2.code) 
		left outer join
		(select code,count(*) bctd,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='0' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date group by code,p_date,flag) tmp1td on (tmp1.code=tmp1td.code and tmp1td.p_date=tmp1.p_date) 
		left outer join
		(select code,count(*) sctd,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='1' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date group by code,p_date,flag) tmp2td on (tmp1.code=tmp2td.code and tmp2td.p_date=tmp1.p_date) 
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='0' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and (dealer like '%机构专用%' or dealer is null) group by code,p_date,flag) tmp3 on (tmp1.code=tmp3.code and tmp1.p_date=tmp3.p_date)
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='1' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and (dealer like '%机构专用%' or dealer is null) group by code,p_date,flag) tmp4 on (tmp1.code=tmp4.code and tmp1.p_date=tmp4.p_date)
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='0' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and dealer like '%交易单元%' group by code,p_date,flag) tmp5 on (tmp1.code=tmp5.code and tmp1.p_date=tmp5.p_date)
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='1' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and dealer like '%交易单元%' group by code,p_date,flag) tmp6 on (tmp1.code=tmp6.code and tmp1.p_date=tmp6.p_date)
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='0' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and dealer like '%总部%' group by code,p_date,flag) tmp7 on (tmp1.code=tmp7.code and tmp1.p_date=tmp7.p_date)
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='1' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and dealer like '%总部%' group by code,p_date,flag) tmp8 on (tmp1.code=tmp8.code and tmp1.p_date=tmp8.p_date)
		) tmp join (select distinct code,name,reason,p_date from longhu_general where reason not like '连续%') t2 on tmp.code=t2.code and tmp.p_date=t2.p_date join (select code,curr_price from prices) t3  on tmp.code=t3.code order by diff1 desc;
" > tmp.sql
mysql -uroot -proot < tmp.sql > tmp.txt
iconv -f utf-8 -t gb18030 tmp.txt > longhu.csv
sed -i "s/\t/,/g" longhu.csv
sed -i "s/<tab>/\t/g" longhu.csv

echo "
use quantum;
select tmp.p_date as 'date',concat('\"<tab>',tmp.code,'\"') code,t2.name,t3.curr_price c_price,'NULL' deal_price,'NULL' as 'volumn(wg)',if(abs(buy_amount-sold_amount)>1,round(buy_amount-sold_amount,0),buy_amount-sold_amount) as 'amount(wy)','NULL' as 'ratio(close/deal)',bc bc15,sc sc15,diff '1_diff15',if(bctd is null,0,bctd) bc1,if(sctd is null,0,sctd) sc1,if(diff1 is null,0,diff1) diff1,if(buy_amount>1,round(buy_amount,0),buy_amount) as 'buy_amount(wy)',if(sold_amount>1,round(sold_amount,0),sold_amount) as 'sold_amount(wy)',if(abs(buy_amount-sold_amount)>1,round(buy_amount-sold_amount,0),buy_amount-sold_amount) as 'net_amount15(wy)',if(buy_amount1 is null,0,round(buy_amount1,0)) as 'buy_amount1(wy)',if(sold_amount1 is null,0,round(sold_amount1,0)) as 'sold_amount1(wy)',if(buy_amount1 is null,0,if(abs(buy_amount1-sold_amount1)>1,round(buy_amount1-sold_amount1,0),buy_amount1-sold_amount1)) as 'net_amount(wy)(buy_amount-sold_amount)',if(abs(net_jigou) > 1 ,round(net_jigou,0),net_jigou) net_jigou,if(abs(net_jiaoyidanyuan)>1,round(net_jiaoyidanyuan,0),net_jiaoyidanyuan) net_jiaoyidanyuan,if(abs(net_zongbu)>1,round(net_zongbu,0),net_zongbu) net_zongbu,concat('\"',reason,'\"') as reason from 
(select tmp1.code,bc,sc,bc-sc diff,tmp1td.buy_amount+tmp2td.buy_amount buy_amount1,tmp1td.sold_amount+tmp2td.sold_amount sold_amount1,bctd,sctd,bctd-sctd diff1,tmp1.p_date,tmp1.buy_amount+tmp2.buy_amount as buy_amount,tmp1.sold_amount+tmp2.sold_amount as sold_amount,tmp3.buy_amount+tmp4.buy_amount-tmp3.sold_amount-tmp4.sold_amount as 'net_jigou',tmp5.buy_amount+tmp6.buy_amount-tmp5.sold_amount-tmp6.sold_amount as 'net_jiaoyidanyuan',tmp7.buy_amount+tmp8.buy_amount-tmp7.sold_amount-tmp8.sold_amount as 'net_zongbu' from 
		(select code,flag,count(*) bc,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,max(p_date) p_date from longhu_detail where flag='0' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date group by code,flag) tmp1 join
		(select code,flag,count(*) sc,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,max(p_date) from longhu_detail where flag='1' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date group by code,flag) tmp2 on (tmp1.code=tmp2.code) 
		left outer join
		(select code,count(*) bctd,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='0' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date group by code,p_date,flag) tmp1td on (tmp1.code=tmp1td.code and tmp1.p_date=tmp1td.p_date) 
		left outer join
		(select code,count(*) sctd,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='1' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date group by code,p_date,flag) tmp2td on (tmp1.code=tmp2td.code and tmp1.p_date=tmp2td.p_date) 
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='0' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and (dealer like '%机构专用%' or dealer is null) group by code,p_date,flag) tmp3 on (tmp1.code=tmp3.code and tmp1.p_date=tmp3.p_date)
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='1' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and (dealer like '%机构专用%' or dealer is null) group by code,p_date,flag) tmp4 on (tmp1.code=tmp4.code and tmp1.p_date=tmp4.p_date)
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='0' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and dealer like '%交易单元%' group by code,p_date,flag) tmp5 on (tmp1.code=tmp5.code and tmp1.p_date=tmp5.p_date)
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='1' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and dealer like '%交易单元%' group by code,p_date,flag) tmp6 on (tmp1.code=tmp6.code and tmp1.p_date=tmp6.p_date)
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='0' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and dealer like '%总部%' group by code,p_date,flag) tmp7 on (tmp1.code=tmp7.code and tmp1.p_date=tmp7.p_date)
		left outer join
		(select code,sum(buy_amount) buy_amount,sum(sold_amount) sold_amount,p_date from longhu_detail where flag='1' and str_to_date('${YESTERDAY}','%Y%m%d')<=p_date and dealer like '%总部%' group by code,p_date,flag) tmp8 on (tmp1.code=tmp8.code and tmp1.p_date=tmp8.p_date)
		) tmp join (select distinct code,name,reason,p_date from longhu_general where reason like '连续%') t2 on tmp.code=t2.code and tmp.p_date=t2.p_date join (select code,curr_price from prices) t3  on tmp.code=t3.code order by diff1 desc;
" > tmp.sql
mysql -uroot -proot < tmp.sql > tmp_lx.txt
iconv -f utf-8 -t gb18030 tmp_lx.txt > longhu_lx.csv
sed -i "s/\t/,/g" longhu_lx.csv
sed -i "s/<tab>/\t/g" longhu_lx.csv
sed -i "1d" longhu_lx.csv

echo "">> longhu.csv
echo "">> longhu.csv
echo "">> longhu.csv
cat longhu_lx.csv>>longhu.csv
