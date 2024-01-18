#http://genome.ucsc.edu/cgi-bin/hgTables

# wget -c -O mm9.refGene.txt.gz http://hgdownload.soe.ucsc.edu/goldenPath/mm9/database/refGene.txt.gz
# wget -c -O mm10.refGene.txt.gz http://hgdownload.soe.ucsc.edu/goldenPath/mm10/database/refGene.txt.gz
wget -c -O hg19.refGene.txt.gz http://hgdownload.soe.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz
wget -c -O hg38.refGene.txt.gz http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/refGene.txt.gz


# https://github.com/counsyl/hgvs/blob/master/pyhgvs/utils.py
# http://genome.ucsc.edu/FAQ/FAQformat.html#GenePredExt

    # Column definitions:
    # 0. uint undocumented id
    # 1. string name;             "Name of gene (usually transcript_id from GTF)"
    # 2. string chrom;                "Chromosome name"
    # 3. char[1] strand;              "+ or - for strand"
    # 4. uint txStart;                "Transcription start position"
    # 5. uint txEnd;                  "Transcription end position"
    # 6. uint cdsStart;               "Coding region start"
    # 7. uint cdsEnd;                 "Coding region end"
    # 8. uint exonCount;              "Number of exons"
    # 9. uint[exonCount] exonStarts;  "Exon start positions"
    # 10. uint[exonCount] exonEnds;   "Exon end positions"
    # 11. uint id;                    "Unique identifier"
    # 12. string name2;               "Alternate name (e.g. gene_id from GTF)"
    # 13. string cdsStartStat;        "enum('none','unk','incmpl','cmpl')"
    # 14. string cdsEndStat;          "enum('none','unk','incmpl','cmpl')"
    # 15. lstring exonFrames;         "Exon frame offsets {0,1,2}"
