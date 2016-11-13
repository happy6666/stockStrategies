DIR=/home/yiwen/stockStrategies/options/script
TODAY=$(date --date='1 day ago' +'%Y%m%d')

DATA_FILE_JIAOYI='../data/all_jiaoyi_data.asv'
DATA_FILE_JIESUAN='../data/all_jiesuan_data.asv'
DATA_FILE_HUIZONG_JIESUAN='../data/all_huizongjiesuan_data.asv'
DATA_FILE_RIJIAOYI='../data/all_rijiaoyi_data.asv'
DATA_FILE_YEWU='../data/all_yewu_data.asv'
DATA_FILE_DALIAN='../data/all_dalian_tongji_data.asv'
DATA_FILE_ZZJIESUAN='../data/all_zhengzhou_jiesuan_data.asv'
DATA_FILE_ZZDAILY='../data/all_zhengzhou_daily_data.asv'
DATA_FILE_ZJDAILY='../data/all_zhongjin_daily_data.asv'

LOG_FILE_JIAOYI="../log/${TODAY}_jiaoyi.log"
LOG_FILE_JIESUAN="../log/${TODAY}_jiesuan.log"
LOG_FILE_HUIZONG_JIESUAN="../log/${TODAY}_huizongjiesuan.log"
LOG_FILE_RIJIAOYI="../log/${TODAY}_rijiaoyi.log"
LOG_FILE_YEWU="../log/${TODAY}_yewu.log"
LOG_FILE_DALIAN="../log/${TODAY}_daliantongji.log"
LOG_FILE_ZZJIESUAN="../log/${TODAY}_zzjiesuan.log"
LOG_FILE_ZZDAILY="../log/${TODAY}_zzdaily"
LOG_FILE_ZJDAILY="../log/${TODAY}_zjdaily"

cd $DIR
echo $TODAY

python jiaoyi_parameter.py $TODAY $DATA_FILE_JIAOYI &>${LOG_FILE_JIAOYI} &
python jiesuan_parameter.py $TODAY $DATA_FILE_JIESUAN &>${LOG_FILE_JIESUAN} &
python huizongjiesuan_parameter.py $TODAY $DATA_FILE_HUIZONG_JIESUAN &>${LOG_FILE_HUIZONG_JIESUAN} &
python rijiaoyi_parameter.py $TODAY $DATA_FILE_RIJIAOYI &>${LOG_FILE_RIJIAOYI} &
python yewu_parameter.py $TODAY $DATA_FILE_YEWU &>${LOG_FILE_YEWU} &
python dalian_tongji_parameter.py $TODAY $DATA_FILE_DALIAN &>${LOG_FILE_DALIAN} &
python zzjiesuan_parameter.py $TODAY $DATA_FILE_ZZJIESUAN &>${LOG_FILE_ZZJIESUAN} &
python zzdaily_price.py $TODAY $DATA_FILE_ZZDAILY &>${LOG_FILE_ZZDAILY} &
python zj_daily_price.py $TODAY $DATA_FILE_ZJDAILY &>${LOG_FILE_ZJDAILY} &

wait
