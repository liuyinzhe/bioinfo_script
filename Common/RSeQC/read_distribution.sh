sample=$(echo $(basename $PWD))
binary=/software/rseqc/bin
${binary}/read_distribution.py \
  -i ${sample}.sorted.bam \
  -r /project/RNA_seq/ref/hg38.ensembl.bed >read_distribution.report.txt
