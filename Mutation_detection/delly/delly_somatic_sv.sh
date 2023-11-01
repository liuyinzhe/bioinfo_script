#!/bin/bash

DELLY_INSTALL_PATH=/data/binary
sample=sample
REF=/data/database/genome/hg38.fa
DELLY_PATH=/data/project/projectA/01.call/delly

PATH=/data/binary:$PATH

cd ${DELLY_PATH}/${sample}

${DELLY_INSTALL_PATH}/delly call  \
  --genome ${REF} \
  --exclude  /data/database/delly/human.hg38.excl.tsv \
  --outfile ${DELLY_PATH}/${sample}/delly.${sample}.somatic.unfilter.bcf \
  /data/project/projectA/04.BQSR/${sample}/${sample}.sorted.rmdup.BQSR.bam \
  /data/project/projectA/04.BQSR/control_sample/control_sample.sorted.rmdup.BQSR.bam 

echo -e "${sample}\ttumor" > samples.tsv
echo -e "control_sample\tcontrol" >>samples.tsv

${DELLY_INSTALL_PATH}/delly filter \
    -f somatic \
    -o ${DELLY_PATH}/${sample}/delly.${sample}.somatic.filter.bcf  \
    -s samples.tsv \
    ${DELLY_PATH}/${sample}/delly.${sample}.somatic.unfilter.bcf 

bcftools  filter  -i'FILTER=="PASS"' -Oz -o delly.${sample}.somatic.PASS.vcf.gz   delly.${sample}.somatic.filter.vcf.gz 
bcftools index delly.${sample}.somatic.filter.vcf.gz 

sansa annotate -g Homo_sapiens.GRCh37.87.gtf.gz delly.${sample}.somatic.PASS.vcf.gz

# gtf hg19
# https://grch37.ensembl.org/Homo_sapiens/Info/Index
# https://ftp.ensembl.org/pub/grch37/current/gtf/homo_sapiens/Homo_sapiens.GRCh37.87.gtf.gz


# gtf hg38
# https://www.ensembl.org/Homo_sapiens/Info/Index
# https://ftp.ensembl.org/pub/release-110/gtf/homo_sapiens/Homo_sapiens.GRCh38.110.gtf.gz


# hg19 gnomad 2.1 SV
# https://gnomad.broadinstitute.org/downloads#v2
# https://datasetgnomad.blob.core.windows.net/dataset/papers/2019-sv/gnomad_v2.1_sv.sites.vcf.gz

# hg38 liftover 
# https://gnomad.broadinstitute.org/downloads#v2-liftover-structural-variants
# 
#https://ftp.ncbi.nlm.nih.gov/pub/dbVar/data/Homo_sapiens/by_study/vcf/nstd166*
# https://ftp.ncbi.nlm.nih.gov/pub/dbVar/data/Homo_sapiens/by_study/vcf/nstd166.GRCh38.variant_call.vcf.gz
# https://ftp.ncbi.nlm.nih.gov/pub/dbVar/data/Homo_sapiens/by_study/vcf/nstd166.GRCh38.variant_call.vcf.gz.tbi
