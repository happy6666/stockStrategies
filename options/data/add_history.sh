#!/bin/bash

DIR=/home/yiwen/stockStrategies/options/data
cd $DIR

if [[ "$#" -lt "1" ]]
then
	echo "Require 1 argument. Read $#"
	exit 0
fi

file=$1

cat "${file}" > "all/${file}.csv"
cat "20160704-20150522/${file}" >> "all/${file}.csv"
cat "20150521-20060821/${file}" >> "all/${file}.csv"
cat "history/${file}" >> "all/${file}.csv"
sed -i.bk1 s/,//g "all/${file}.csv"
python convert_percent_num.py "all/${file}.csv" "all/${file}.np.csv"
sed -i.bk2 s//,/g "all/${file}.np.csv"
iconv -f utf-8 -t gb18030 "all/${file}.np.csv" > "done/${file}.gb.csv"
