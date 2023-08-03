makeblastdb -in genome.fa -dbtype nucl   -input_type fasta  -out db
blastn -db db -query query.fa -task blastn-short -outfmt 6 -evalue 1e-5 -num_threads 4  -out result.blast
