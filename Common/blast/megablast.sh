#!/bin/bash


cd /data/work/megeblast/
echo "start time: `date +"%Y-%m-%d %H:%M:%S"`" >time.log

/data/Common/bin/blastn \
   -task megablast  \
   -db /data/database/nucl/NT \
   -query query.fa \
   -outfmt  '6 qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore qcovs qcovhsp qcovus' \
   -subject_besthit \
   -evalue 1e-100 \
   -max_target_seqs 100 \
   -num_threads 20 \
    -out result.blast

echo "end time: `date +"%Y-%m-%d %H:%M:%S"`" >>time.log

python3 megablast_ann_tax.py

cut -f 22 result.xls  |sort | uniq -c |sort -k1nr >summary

# preparation
#wget https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip
#wget https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/dead_nucl.accession2taxid.gz
#unzip taxdmp.zip
#grep "scientific name" names.dmp | awk -F"|" '{print $1,$2}' |sed 's/\t \t/\t/' > tax_id2name.txt
