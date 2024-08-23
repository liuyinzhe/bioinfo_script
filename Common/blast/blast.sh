#makeblastdb -in  all_database.fa -dbtype nucl   -input_type fasta  -out db
makeblastdb -in  all_database.fa -dbtype prot   -input_type fasta  -out db

blastp -db db -query all.faa -outfmt 6 -evalue 1e-5 -num_threads 4  -out result.blast


# Blast++与Diamond区别之一 qcovs
# https://www.jianshu.com/p/9856fdce267b
##Blast++
#--outfmt  '6 qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore qcovs qcovhsp'

#Diamond
#--outfmt  6 qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore qcovhsp

#注意细节，Diamond不需要单引号，少了一个 qcovs 的计算，源码也是没写

# 最优blast 比对
# python -m jcvi.formats.blast best -n 1 raw.blast.txt
