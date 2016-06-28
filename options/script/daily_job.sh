DIR=/home/yiwen/stockStrategies/options/script
TODAY=$(date --date='1 day ago' +'%Y%m%d')
DATA_FILE='../data/all_jiaoyi_data.asv'
LOG_FILE="../log/${TODAY}.log"
cd $DIR
echo $TODAY
python jiaoyi_parameter.py $TODAY $DATA_FILE 1>${LOG_FILE} 2>${LOG_FILE}
