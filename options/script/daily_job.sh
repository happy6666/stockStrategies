DIR=/home/yiwen/stockStrategies/options/script
TODAY=$(date --date='1 day ago' +'%Y%m%d')
DATA_FILE_JIAOYI='../data/all_jiaoyi_data.asv'
DATA_FILE_JIESUAN='../data/all_jiesuan_data.asv'
DATA_FILE_HUIZONG_JIESUAN='../data/all_huizongjiesuan_data.asv'
LOG_FILE_JIAOYI="../log/${TODAY}_jiaoyi.log"
LOG_FILE_JIESUAN="../log/${TODAY}_jiesuan.log"
LOG_FILE_HUIZONG_JIESUAN="../log/${TODAY}_huizongjiesuan.log"
cd $DIR
echo $TODAY
python jiaoyi_parameter.py $TODAY $DATA_FILE_JIAOYI 1>${LOG_FILE_JIAOYI} 2>${LOG_FILE_JIAOYI}
python jiesuan_parameter.py $TODAY $DATA_FILE_JIESUAN 1>${LOG_FILE_JIESUAN} 2>${LOG_FILE_JIESUAN} 
python huizongjiesuan_parameter.py $TODAY $DATA_FILE_JIESUAN 1>${LOG_FILE_JIESUAN} 2>${LOG_FILE_JIESUAN} 
