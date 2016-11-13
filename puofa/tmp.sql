
use quantum;
select concat('"<tab>',code,'"') code,name,c_price as 'c_price(fuquan)',faxing_price from (select a.code,a.name,a.price as c_price,b.price as faxing_price from (select * from fuquanprice where p_date='2016-11-11') a join puofa b on (a.code=b.code) ) tmp where faxing_price<=c_price and c_price!=0;

