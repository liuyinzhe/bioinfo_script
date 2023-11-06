#!/bin/bash

export PATH=/data/database/miniconda/envs/metaphlan4/bin:$PATH

METADIR=/data/

cd ${METADIR}/metaphlan4
mkdir -p bowtie2  profiles
rm -rf batch_metaphlan4.sh
while read sample ;
do
echo -e "/data/miniconda/envs/metaphlan4/bin/metaphlan \
   ${METADIR}/output/kneaddata/${sample}.1_kneaddata_paired_2.fastq,${METADIR}/output/kneaddata/${sample}.1_kneaddata_paired_2.fastq \
  --nproc 10 \
  --input_type fastq \
  --bowtie2db /data/miniconda/envs/metaphlan4/lib/python3.7/site-packages/metaphlan/metaphlan_databases \
  --index mpa_vOct22_CHOCOPhlAnSGB_202212 \
  -o profiles/${sample}_profiled.tsv \
  --bowtie2out bowtie2/${sample}.bowtie2.bz2  >${METADIR}/output/metaphlan4/log 2>${METADIR}/output/metaphlan4/err " >>batch_metaphlan4.sh
done <sample.lst
