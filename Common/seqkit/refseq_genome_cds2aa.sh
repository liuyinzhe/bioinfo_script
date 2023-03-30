awk '{if(/>/){print ">"$2}else{print ;}}' X_cds_from_genomic.fna  |sed -e 's/\[gene=//g'  -e 's/]//g' > X_cds_from_genomic.fna 
seqkit translate  X_cds_from_genomic.fna   > X_cds_from_genomic.faa 
sed -i 's/\*//g' X_cds_from_genomic.faa 
