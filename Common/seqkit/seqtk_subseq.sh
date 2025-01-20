
samtools view -F 4 sample.target.bam | awk '{print $1}' | sort | uniq > name.list

seqtk subseq sample.R1.fastq.gz name.list > sample.1.fq
seqtk subseq sample.R2.fastq.gz name.list > sample.2.fq
gzip sample.1.fq
gzip sample.2.fq
