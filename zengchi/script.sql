use quantum;
select tmp2.code,amount,avg_price,curr_price from (
		select * from 
		(
		 select a.code ,amount,amount/c as avg_price from (
		 select code,p_name,sum(count*avg_price) as amount from 
			(select * from zengchi where p_date>=str_to_date('20140601','%Y%m%d') and count>0) tmp 
			group by code,p_name) a,
		 (select code,p_name,sum(count) as c from 
			(select * from zengchi where p_date>=str_to_date('20140601','%Y%m%d') and count>0) tmp 
			group by code,p_name) b where a.code=b.code and a.p_name=b.p_name
		) tmp1 where amount>=1000000) tmp3
, (select code,curr_price from prices) tmp2 where tmp3.code=tmp2.code and tmp3.avg_price>tmp2.curr_price;
