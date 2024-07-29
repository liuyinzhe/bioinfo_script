PJ_ID=x
sample=a
ulimit -HSn 4096 ;
mkdkr -p ${PJ_ID}/02.bwa/${sample}/${sample}/tmp

bwa-mem2 mem \
   -t 2 -M \
   -Y /data/database/genome/bwamem2/hg38.fa \
   -R "@RG\tID:${PJ_ID}\tLB:NGS\tPL:Illumina\tSM:${sample}" \
   ${PJ_ID}/01.QC/${sample}/${sample}.clean.1.fq.gz \
   ${PJ_ID}/01.QC/${sample}/${sample}.clean.2.fq.gz | \
sambamba view -q -t 1 -f bam -S \
   -o ${PJ_ID}/02.bwa/${sample}/${sample}.bam /dev/stdin && \
sambamba sort -q \
   --tmpdir=${PJ_ID}/02.bwa/${sample}/tmp \
   -t 2 -o ${PJ_ID}/02.bwa/${sample}/${sample}.sorted.bam \
   ${PJ_ID}/02.bwa/${sample}/${sample}.bam && \
   rm -rf ${PJ_ID}/02.bwa/${sample}/${sample}.bam
