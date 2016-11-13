#!/bin/bash
DIR=/home/yiwen/stockStrategies/options/script
TODAY=$(date --date="1 day ago" +"%Y%m%d")

DATA_FILE_ZJDAILY='../data/all_zhongjin_daily_data.asv'

LOG_FILE_ZJDAILY="../log/${TODAY}_zjdaily"

cd $DIR
declare -i DOW

for i in $(seq 0 10855 )
do
    TODAY=$(date --date="$i day ago" +'%Y%m%d')
    DOW=$(date --date="$i day ago" +'%u')
    if [ $DOW -ge 1 ]
    then
        if [ $DOW -le 5 ]
        then
            echo $TODAY
			python zj_daily_price.py $TODAY $DATA_FILE_ZJDAILY &>${LOG_FILE_ZJDAILY} &
			wait
        fi
    fi
done
