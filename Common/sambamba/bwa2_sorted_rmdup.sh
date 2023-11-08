reference=hg38.fa
sample=AAAAA

 bwa-mem2 mem -t 4 \
  -M -Y ${reference} \
  -R "@RG\tID:20231106\tLB:NGS\tPL:Illumina\tSM:Normal" \
  ${sample}.clean.1.fq \
  ${sample}.clean.2.fq \
  | sambamba view -q -t 4 -f bam -S /dev/stdin -l 0 -o /dev/stdout \
  | sambamba sort  -q --tmpdir=${PWD}/${sample}/tmp -t 4 /dev/stdin -o  ${sample}/${sample}.sorted.bam  && \
   sambamba markdup -q --tmpdir=${PWD}/tmp  -t 4 ${sample}/${sample}.sorted.bam ${sample}/${sample}.sorted.rmdup.bam && rm -rf ${sample}/${sample}.sorted.bam*
   
