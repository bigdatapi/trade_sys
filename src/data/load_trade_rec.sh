#!/bin/sh

if [ $# -ne 1 ]; then
    echo "usage : $0 ./SOURCE_TRADE_REC_FILE\n"
    exit 1
fi

input_file=$1
if [ ! -f ./$input_file ]; then
    echo "input_file $input_file not exists\n"
    exit 2
fi

echo "input file : ./$input_file"
dos2unix ./$input_file >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "dos2unix for $input_file fail"
    exit 3
else
    echo "dos2unix for $input_file ok"
fi

iconv -f gbk -t utf-8 ./$input_file > xxx.txt
if [ $? -ne 0 ]; then
    echo "iconv for $input_file fail"
    exit 4
else 
    echo "iconv for $input_file ok"
fi

python _load_trade_rec.py xxx.txt
if [ -z $? ]; then
    echo "python _load_trade_rec.py xxx.txt ok"
    exit 0
else 
    echo "python _load_trade_rec.py xxx.txt fail"
    exit 5
fi

