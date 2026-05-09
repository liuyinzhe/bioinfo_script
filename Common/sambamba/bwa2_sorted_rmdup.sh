reference=hg38.fa
sample=AAAAA

 ulimit -HSn 4096 ;
 bwa-mem2 mem -t 4 \
  -M -Y ${reference} \
  -R "@RG\tID:20231106\tLB:NGS\tPL:Illumina\tSM:Normal" \
  ${sample}.clean.1.fq \
  ${sample}.clean.2.fq \
  | sambamba view -q -t 4 -f bam -S /dev/stdin -l 0 -o /dev/stdout \
  | sambamba sort  -q -m 8G --tmpdir=${PWD}/${sample}/tmp -t 4 /dev/stdin -o  ${sample}/${sample}.sorted.bam  && \
   sambamba markdup -q   --hash-table-size 524288 --overflow-list-size 600000 \
  --tmpdir=${PWD}/tmp  -t 4 ${sample}/${sample}.sorted.bam ${sample}/${sample}.sorted.rmdup.bam && rm -rf ${sample}/${sample}.sorted.bam*

# sambamba  markdup   in mode `w+' (Too many open files)
# https://github.com/biod/sambamba/issues/177
# try --overflow-list-size 600000; There is no upper threshold, and another suggestion is to increase --hash-table-size as well
