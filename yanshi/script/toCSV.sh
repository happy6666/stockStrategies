#!/bin/bash

while read line
do
	cat "$line" > "${line}.csv"
	sed -i.bk1 s,/,,g "${line}.csv"
	sed -i.bk2 s//,/g "${line}.csv"
	iconv -f utf-8 -t gb18030 "${line}.csv" > "${line}.gb.csv"
done
