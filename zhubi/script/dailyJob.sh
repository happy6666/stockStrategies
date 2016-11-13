#!/bin/bash
dir=/home/yiwen/stockStrategies/zhubi/script
cd $dir

today=$(date +'%Y-%m-%d')
script='python /home/yiwen/stockStrategies/zhubi/script/dump.py'
while read -s line || [[ -n "$line" ]];
do
	echo $line
	$script $line $today
done <$1
