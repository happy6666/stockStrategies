
use quantum;
select p_date as 'date',concat('"<tab>',t0.code,'"') as code,name,curr_price as c_price,real_price deal_price,curr_price/real_price as '1_ratio(close/deal)',state,type,method,shangshi_date as '2_shangshi_date' from (select code,state,type,method,real_price,shangshi_date from addition) t0 join (select code,name,curr_price,p_date from prices) t1 on t0.code=t1.code where curr_price/real_price<=1 and curr_price!=0 order by type desc,curr_price/real_price,shangshi_date desc;

