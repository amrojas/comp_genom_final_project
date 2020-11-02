#!/bin/bash

KMERS="0"
BUCKETS="32768 65536 131072 262144" # 1048576 33554432 1073741824"
BUCKET_SIZES="4"
MAX_ITERS="500"
FP_SIZES=`seq 1 1 20` # [1:20]

APP_ROOT="$(dirname "$(dirname "$(readlink -fm "$0")")")"
timestamp=$(date +%y%m%d-%H%M%S)
OUTPUT="$APP_ROOT/eval/result-$timestamp.csv"

for k in $KMERS
do
    for b in $BUCKETS 
    do
        for s in $BUCKET_SIZES 
        do
            for i in $MAX_ITERS 
            do
                for f in $FP_SIZES 
                do
                    echo "experimnenting with k=$k, b=$b, s=$s, i=$i, f=$f"
                    python3 $APP_ROOT/src/main.py --datafiles synthetic.fastq --create-cuckoo-filter -k $k -b $b -s $s -i $i -f $f &>> $OUTPUT
                done
            done
        done
    done
done
