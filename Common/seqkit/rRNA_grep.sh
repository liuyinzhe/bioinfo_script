rna_fna=$1
zcat ${rna_fna} | grep "^>" | grep "gbkey=rRNA" | awk '{print $1}'|sed 's/>//g' > id.list


seqkit grep -f id.list ${rna_fna} > rRNA.fa
bowtie2-build  rRNA.fa rRNA
