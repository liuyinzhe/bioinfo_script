
# minimap2比对
minimap2 -cx asm5 --cs QUERY_FASTA.fa REFERENCE_FASTA.fa > PAF_FILE.paf

# transanno创建chain文件
transanno minimap2chain PAF_FILE.paf --output CHAINFILE.chain


# Convert GENCODE/Ensembl GFF3/GTF
# Prepare GENCODE or Ensembl GFF3/GTF file, a query FASTA, a reference FASTA, a chain file.
# Run transanno transanno liftgene GENCODE.gtf.gz --chain CHAINFILE.chain --failed FAILED.gtf.gz --output SUCCEEDED.gtf.gz
