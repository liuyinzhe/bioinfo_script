#makeblastdb -in  all_database.fa -dbtype nucl   -input_type fasta  -out db
makeblastdb -in  all_database.fa -dbtype prot   -input_type fasta  -out db

blastp -db db -query all.faa -outfmt 6 -evalue 1e-5 -num_threads 4  -out result.blast
