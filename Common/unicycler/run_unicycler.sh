
# ngs PE
unicycler \
  --keep 1 \
  --no_pilon \
  --no_correct \
  --min_kmer_frac 0.6 \
  --max_kmer_frac 0.99 \
  --kmer_count 3 \
  --min_fasta_length 500 \
  --threads 8 \
  --short1 sample.1.fastq.gz \
  --short2 sample.2.fastq.gz \
  --out spades_out/sample 
