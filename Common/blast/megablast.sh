#!/bin/bash

cd /data/work/megeblast/
echo "start time: `date +"%Y-%m-%d %H:%M:%S"`" >time.log

/data/Common/bin/blastn \
   -db /data/database/nucl/NT \
   -query query.fa \
   -outfmt  '6 qseqid sseqid pident length mismatch gapopen qlen qstart qend slen sstart send evalue bitscore qcovs qcovhsp qcovus' \
   -subject_besthit \
   -evalue 1e-100 \
   -max_target_seqs 100 \
   -num_threads 20 \
    -out result.blast

echo "end time: `date +"%Y-%m-%d %H:%M:%S"`" >>time.log
