#!/bin/bash

export PATH=/data/envs/microbe/bin:$PATH


startTime=`date '+%Y-%m-%d %H:%M:%S'`
startTime_s=`date +%s`

sortmerna --index 0 --threads 8 \
--ref /data/database/rRNA_databases/smr_v4.3_default_db.fasta \
--workdir /data3/sortmerna/sample/ \
--kvdb /data/database/rRNA_databases/kvdb  \
--idx-dir /data/database/rRNA_databases/idx  \
--readb /data/database/rRNA_databases/readb  \
--reads sample.1_kneaddata_paired_1.fastq \
--reads sample.1_kneaddata_paired_2.fastq \
--aligned "sample/rRNA" --other "sample/clean" --paired_in --fastx --out2  && \
gzip sample/clean.fastq && \
rm -rf sample/rRNA.fastq

#    --kvdb            PATH        Optional  Directory for Key-value database            WORKDIR/kvdb
#    --idx-dir         PATH        Optional  Directory for storing Reference index.      WORKDIR/idx
#    --readb           PATH        Optional  Storage for pre-processed reads             WORKDIR/readb/


endTime=`date '+%Y-%m-%d %H:%M:%S'`
endTime_s=`date +%s`
sumTime=$[ $endTime_s - $startTime_s ]
days=$((sumTime / 60 / 60 / 24)) 
hours=$(( (sumTime / 60 / 60 ) % 24 ))
minutes=$((sumTime / 60 % 60)) 
seconds=$((sumTime % 60)) 

echo "$startTime ---> $endTime" "Total:$days days,$hours hours,$minutes minutes and $seconds seconds"
