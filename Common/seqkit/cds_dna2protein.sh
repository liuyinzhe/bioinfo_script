awk '{if(/>/){print ">"$2}else{print ;}}' GCF_018294505.1_IWGSC_CS_RefSeq_v2.1_cds_from_genomic.fna  |sed -e 's/\[gene=//g'  -e 's/]//g' > IWGSC_CS_RefSeq_v2.1_cds_from_genomic.fna 
seqkit translate   IWGSC_CS_RefSeq_v2.1_cds_from_genomic.fna > IWGSC_CS_RefSeq_v2.1_cds_from_genomic.faa
