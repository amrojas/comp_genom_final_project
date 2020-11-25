#!/bin/bash

EXPECTED_ITEMS="10000000"
FP_PROB="0.00001 0.0001 0.001 0.01 0.1" # 1048576 33554432 1073741824"

APP_ROOT="$(dirname "$(dirname "$(readlink -fm "$0")")")"
timestamp=$(date +%y%m%d-%H%M%S)

OUTPUT1="$APP_ROOT/eval/result-bl-$timestamp.csv"
OUTPUT2="$APP_ROOT/eval/result-cu-$timestamp.csv"
OUTPUT3="$APP_ROOT/eval/result-cb-$timestamp.csv"
for p in $FP_PROB
do
    echo "experimenting with e=$EXPECTED_ITEMS, p=$p, bloom"
    python3 $APP_ROOT/src/main.py --datafiles synthetic-large.fastq --auto --create-bloom-filter -e $EXPECTED_ITEMS -p $p &>> $OUTPUT1
    echo "experimenting with e=$EXPECTED_ITEMS, p=$p, cuckoo"
    python3 $APP_ROOT/src/main.py --datafiles synthetic-large.fastq --auto --create-cuckoo-filter -e $EXPECTED_ITEMS -p $p &>> $OUTPUT2
    echo "experimenting with e=$EXPECTED_ITEMS, p=$p, cuckoo-bit"
    python3 $APP_ROOT/src/main.py --datafiles synthetic-large.fastq --auto --create-cuckoo-filter-bit -e $EXPECTED_ITEMS -p $p &>> $OUTPUT3
done
