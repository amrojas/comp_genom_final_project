#!/bin/bash

EXPECTED_ITEMS="10000000"
FP_PROB=0.01 # 1048576 33554432 1073741824"

APP_ROOT="$(dirname "$(dirname "$(readlink -fm "$0")")")"
timestamp=$(date +%y%m%d-%H%M%S)

OUTPUT1="$APP_ROOT/eval/result-tab3-$timestamp.csv"
echo "k,buckets,fp_size,buck_size,iterations,items,constr_speed,load_factor, total_size_bytes, bits_per_item, false_positive_rate" >> $OUTPUT1
echo "experimenting with e=$EXPECTED_ITEMS, p=$p, bloom"
python3 $APP_ROOT/src/main.py --datafiles synthetic-large.fastq --auto --create-bloom-filter -e $EXPECTED_ITEMS -p $FP_PROB -q fp_dataset.fastq --fp-query &>> $OUTPUT1
echo "experimenting with e=$EXPECTED_ITEMS, p=$p, cuckoo"
python3 $APP_ROOT/src/main.py --datafiles synthetic-large.fastq --create-cuckoo-filter -b 90753 -s 4 -q fp_dataset.fastq --fp-query &>> $OUTPUT1
echo "experimenting with e=$EXPECTED_ITEMS, p=$p, cuckoo-bit"
python3 $APP_ROOT/src/main.py --datafiles synthetic-large.fastq --create-cuckoo-filter-bit -s 4 -b 715000 -e $EXPECTED_ITEMS -p $FP_PROB -q fp_dataset.fastq --fp-query &>> $OUTPUT1
echo "experimenting with e=$EXPECTED_ITEMS, p=$p, cuckoo-stash"
python3 $APP_ROOT/src/main.py --datafiles synthetic-large.fastq --create-cuckoo-filter -b 90752 -s 4 --stash 50 -e $EXPECTED_ITEMS -p $FP_PROB -q fp_dataset.fastq --fp-query &>> $OUTPUT1
echo "line2=Bloom Filter, line3=CuckooFilter, line4=CuckooFilter(Bit), line5=StashedCuckooFilter(s=50)"
