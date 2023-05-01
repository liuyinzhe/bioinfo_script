
# CDS to gene (Prot)
gffread GRCh38.gtf -g GRCh38.fa -y GRCh38.protein.fa

# CDS (DNA)
gffread GRCh38.gtf -g GRCh38.fa -x GRCh38.cds.fa

# transcripts (DNA)
gffread GRCh38.gtf -g GRCh38.fa -w GRCh38.transcripts.fa
