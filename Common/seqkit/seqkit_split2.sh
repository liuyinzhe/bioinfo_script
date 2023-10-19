# For FASTQ files (paired-end)
seqkit split2  \
  --by-part  3 \
  --force  \
  -1 sample.clean.1.fq.gz \
  -2 sample.clean.2.fq.gz \
  -O split_result
