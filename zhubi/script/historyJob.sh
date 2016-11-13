#!/bin/bash
dir=/home/yiwen/stockStrategies/zhubi/script
cd $dir

script='python /home/yiwen/stockStrategies/zhubi/script/dump.py'
for i in $(seq 3 3650)
	do
		today=$(date --date="$i day ago" +'%Y-%m-%d')
		dow=$(date --date="$i day ago" +'%u')
		if [ $dow -ge 1 ]
		then
			if [ $dow -le 5 ]
			then 
				echo $today
				while read -s line || [[ -n "$line" ]];
				do
					echo $line
					$script $line $today
				done <$1
			fi
		fi
	done
