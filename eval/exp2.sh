#!/bin/bash

KMERS="0"
STASH="0 50"    # set to 0 to disable stash
BUCKETS="32768 65536 131072 262144" # 1048576 33554432 1073741824"
BUCKET_SIZES="4 8"
MAX_ITERS="500"
FP_SIZES=`seq 1 2 40` # [1:20]

APP_ROOT="$(dirname "$(dirname "$(readlink -fm "$0")")")"
timestamp=$(date +%y%m%d-%H%M%S)

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
                    for st in $STASH
                    do
                        OUTPUT="$APP_ROOT/eval/result-$s-$st-$timestamp.csv"
                        echo "experimnenting with k=$k, b=$b, s=$s, i=$i, f=$f, stash=$st"
                        python3 $APP_ROOT/src/main.py --datafiles synthetic-large.fastq --create-cuckoo-filter -k $k -b $b -s $s -i $i -f $f --stash $st &>> $OUTPUT
                    done
                    
                done
            done
        done
    done
done
