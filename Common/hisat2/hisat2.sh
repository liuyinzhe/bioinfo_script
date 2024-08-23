sample=sample_x
REF=/data/database/hisat2_index/hg38
QC=/data/analysis/quality_control
HISAT=/data/analysis/hisat2
hisat2 -p 2 --dta  -x ${REF} \
  -1 ${QC}/${sample}.clean.1.fq.gz \
  -2 ${QC}/${sample}.clean.2.fq.gz \
  --new-summary --summary-file ${HISAT}/${sample}/${sample}.summary |samtools view -Sb  > ${HISAT}/${sample}/${sample}.bam
