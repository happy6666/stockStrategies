
use quantum;
select a.p_date as 'date',concat('"<tab>',a.code,'"') code,a.name,b.curr_price as c_price,avg_price deal_price,'NULL' as 'volumn(wg)',amount 'amount(wy)',round(amount*avg_price/(c.value/10000)/b.curr_price,5) '1_ratio(deal*amount/(flowvalue*close))',a.obj_name from jupai a join prices b on a.code=b.code join flowvalue c on c.code=a.code where a.p_date >= str_to_date('20160425','%Y%m%d') and b.curr_price<avg_price and length(a.obj_name) <= 13 order by round(amount*avg_price/(c.value/10000)/b.curr_price,5) desc;

