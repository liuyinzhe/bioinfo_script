#!/bin/bash

DELLY_INSTALL_PATH=/data/binary
REF=/data/database/genome/hg38.fa
WORK_PATH=/data/project/

PATH=/data/binary:$PATH
rm -rf batch_delly.sh
while read sample ; do
mkdir -p ${sample}
echo -e "PATH=/data/binary:$PATH ; \
cd ${WORK_PATH}/08.sv/${sample} ;\
${DELLY_INSTALL_PATH}/delly call  \
  --genome ${REF} \
  --exclude  /data/database/delly/human.hg38.excl.tsv \
  --outfile ${WORK_PATH}/08.sv/${sample}/delly.${sample}.germline.unfilter.bcf \
  ${WORK_PATH}/04.bqsr/${sample}/${sample}.sorted.markdup.BQSR.bam && \
${DELLY_INSTALL_PATH}/delly filter \
    -f germline \
    --pass \
    -o ${WORK_PATH}/08.sv/${sample}/delly.${sample}.germline.filter.bcf  \
    ${WORK_PATH}/08.sv/${sample}/delly.${sample}.germline.unfilter.bcf && \
bcftools  filter  -i'FILTER==\"PASS\"' -Oz -o delly.${sample}.germline.PASS.vcf.gz   delly.${sample}.germline.filter.bcf && \
bcftools index delly.${sample}.germline.PASS.vcf.gz && \
sansa annotate \
 -g /data/database/delly/Homo_sapiens.GRCh38.111.gtf.gz \
  delly.${sample}.germline.PASS.vcf.gz " >>batch_delly.sh
done < sample.lst
