#!/bin/bash
DIR=/home/yiwen/stockStrategies/yanshi
NOW=$(date +'%Y%m%d')
cd $DIR

python script/zz_yanshi.py ${NOW} data/zz_yanshi_${NOW}.asv &>log/zz_yanshi.log &
python script/sh_yanshi.py data/sh_yanshi_${NOW}.asv &>log/sh_yanshi.log &
python script/dl_yanshi.py data/dl_yanshi_${NOW}.asv &>log/dl_yanshi.log &
python script/zj_yanshi.py data/zj_yanshi_${NOW}.asv &>log/zj_yanshi.log &

wait
