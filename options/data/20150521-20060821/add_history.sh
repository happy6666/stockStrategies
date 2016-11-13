#!/bin/bash

DIR=/home/yiwen/stockStrategies/options/data/history
cd $DIR

if [[ "$#" -lt "1" ]]
then
	echo "Require 1 argument. Read $#"
	exit 0
fi

file=$1

cat "${file}" >> "../done/${file}.csv"
#cat "../done/${file}" >> ${file}.csv
sed -i.bk1 s/,//g "../done/${file}.csv"
sed -i.bk2 s//,/g "../done/${file}.csv"
iconv -f utf-8 -t gb18030 "../done/${file}.csv" >> "../done/${file}.gb.csv"
