# build mm10
perl annotate_variation.pl -downdb -buildver mm10 -webfrom annovar refGene mousedb

perl annotate_variation.pl --buildver mm10 --downdb seq mousedb/mm10_seq

perl retrieve_seq_from_fasta.pl mousedb/mm10_refGene.txt -seqdir mousedb/mm10_seq -format refGene -outfile mousedb/mm10_refGeneMrna.fa

#http://hgdownload.cse.ucsc.edu/goldenPath/mm10/bigZips/

# https://www.cnblogs.com/Raymontian/p/7113096.html
