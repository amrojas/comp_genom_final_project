#!/bin/bash

EXPECTED_ITEMS="10000000"
FP_PROB=0.01 # 1048576 33554432 1073741824"

APP_ROOT="$(dirname "$(dirname "$(readlink -fm "$0")")")"
timestamp=$(date +%y%m%d-%H%M%S)

OUTPUT1="$APP_ROOT/eval/result-fig6-bl-$timestamp.csv"
OUTPUT2="$APP_ROOT/eval/result-fig6-cu-$timestamp.csv"
OUTPUT3="$APP_ROOT/eval/result-fig6-cb-$timestamp.csv"

echo "experimenting with e=$EXPECTED_ITEMS, p=$FP_PROB, bloom"
python3 $APP_ROOT/src/main.py --datafiles synthetic-large.fastq --auto --create-bloom-filter --query-tput -e $EXPECTED_ITEMS -p $FP_PROB -q fp_dataset.fastq &>> $OUTPUT1
echo "experimenting with e=$EXPECTED_ITEMS, p=$FP_PROB, cuckoo"
python3 $APP_ROOT/src/main.py --datafiles synthetic-large.fastq --auto --create-cuckoo-filter --query-tput -e $EXPECTED_ITEMS -p $FP_PROB -q fp_dataset.fastq &>> $OUTPUT2
echo "experimenting with e=$EXPECTED_ITEMS, p=$FP_PROB, cuckoo-bit"
python3 $APP_ROOT/src/main.py --datafiles synthetic-large.fastq --auto --create-cuckoo-filter-bit --query-tput -e $EXPECTED_ITEMS -p $FP_PROB -q fp_dataset.fastq &>> $OUTPUT3