#!/bin/bash
DIR=/home/yiwen/stockStrategies/options/script
TODAY=$(date --date="1 day ago" +"%Y%m%d")

DATA_FILE_JIAOYI='../data/history/all_jiaoyi_data.asv'
DATA_FILE_JIESUAN='../data/history/all_jiesuan_data.asv'
DATA_FILE_HUIZONG_JIESUAN='../data/history/all_huizongjiesuan_data.asv'
DATA_FILE_RIJIAOYI='../data/history/all_rijiaoyi_data.asv'
DATA_FILE_YEWU='../data/history/all_yewu_data.asv'
DATA_FILE_DALIAN='../data/history/all_dalian_tongji_data.asv'
DATA_FILE_ZZJIESUAN='../data/history/all_zhengzhou_jiesuan_data.asv'

LOG_FILE_JIAOYI="../log/${TODAY}_jiaoyi.hlog"
LOG_FILE_JIESUAN="../log/${TODAY}_jiesuan.hlog"
LOG_FILE_HUIZONG_JIESUAN="../log/${TODAY}_huizongjiesuan.hlog"
LOG_FILE_RIJIAOYI="../log/${TODAY}_rijiaoyi.hlog"
LOG_FILE_YEWU="../log/${TODAY}_yewu.hlog"
LOG_FILE_DALIAN="../log/${TODAY}_daliantongji.hlog"
LOG_FILE_ZZJIESUAN="../log/${TODAY}_zzjiesuan.hlog"

cd $DIR
declare -i DOW

for i in $(seq 7331 10855 )
do
    TODAY=$(date --date="$i day ago" +'%Y%m%d')
    DOW=$(date --date="$i day ago" +'%u')
    if [ $DOW -ge 1 ]
    then
        if [ $DOW -le 5 ]
        then
            echo $TODAY
			python jiaoyi_parameter.py $TODAY $DATA_FILE_JIAOYI &>>${LOG_FILE_JIAOYI} &
            python jiesuan_parameter.py $TODAY $DATA_FILE_JIESUAN &>>${LOG_FILE_JIESUAN} &
            python huizongjiesuan_parameter.py $TODAY $DATA_FILE_HUIZONG_JIESUAN &>>${LOG_FILE_HUIZONG_JIESUAN} &
            python rijiaoyi_parameter.py $TODAY $DATA_FILE_RIJIAOYI &>>${LOG_FILE_RIJIAOYI} &
            python yewu_parameter.py $TODAY $DATA_FILE_YEWU &>>${LOG_FILE_YEWU} &
            python dalian_tongji_parameter.py $TODAY $DATA_FILE_DALIAN &>>${LOG_FILE_DALIAN} &
			python zzjiesuan_parameter.py $TODAY $DATA_FILE_ZZJIESUAN &>>${LOG_FILE_ZZJIESUAN} &
			wait
        fi
    fi
done
