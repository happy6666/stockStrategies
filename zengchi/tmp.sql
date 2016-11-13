
use quantum;
select p_date as 'date',concat('"<tab>',tmp2.code,'"') code,tmp3.name,curr_price as c_price,round(avg_price,2) as deal_price,if(amount/avg_price/10000,round(amount/avg_price/10000,0),amount/avg_price/10000) as 'volume(wg)',if(amount/10000>1,round(amount/10000,0),amount/10000) as 'amount(wy)',round(curr_price/avg_price,2) as 'ratio(close/deal)',tmp3.p_name as 'obj_name',round(avg_price*amount/10000.0/curr_price/tmp4.value*10000,5) as '1_order(amount*deal/flowvalue/close)' from (
		select * from 
		(
		 select a.code,a.name,a.p_name,amount,amount/c as avg_price ,p_date from (
		 select code,name,p_name,sum(count*avg_price) as amount ,p_date from 
			(select * from zengchi where p_date>=str_to_date('20160425','%Y%m%d') and count>0) tmp 
			group by code,p_name) a,
		 (select code,p_name,sum(count) as c from 
			(select * from zengchi where p_date>=str_to_date('20160425','%Y%m%d') and count>0) tmp 
			group by code,p_name) b where a.code=b.code and a.p_name=b.p_name
		) tmp1 where amount>=1000000) tmp3
, (select code,curr_price from prices) tmp2,(select code,value from flowvalue) tmp4 where tmp3.code=tmp2.code and tmp4.code=tmp2.code and tmp3.avg_price>tmp2.curr_price and length(tmp3.p_name)<=10 order by avg_price*amount/10000.0/curr_price/tmp4.value/10000 desc;

