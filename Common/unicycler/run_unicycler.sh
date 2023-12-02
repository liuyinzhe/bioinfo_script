
# ngs
unicycler \
  --no_pilon \
  --no_correct \
  --min_kmer_frac 0.6 \
  --max_kmer_frac 0.99 \
  --kmer_count 3 \
  --min_fasta_length 500 \
  -t 10 \
  -1 sample.1.fastq.gz \
  -2 sample.2.fastq.gz \
  -o spades_out/sample 
