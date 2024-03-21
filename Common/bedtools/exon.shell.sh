#chrom   start    end   stand       transcript_id           gene    exon number  exon_id
#chr1    13221   14409   +       "ENST00000456328.2";    "DDX11L2";      3;      "ENSE00002312635.1"

zcat gencode.v42.annotation.gtf.gz  |grep -v "^#" | awk '$3=="exon"{print }' |cut -f 1,2,4,5,7,9 |cut -d";" -f 1,2,3,4,5,7,8| awk -F" " 'BEGIN{OFS="\t";}{print $1,$3,$4,$5,$9,$13,$17,$19}' >gencode.exon.bed


cut -f 1,2,3 gencode.exon.bed |sort -k1V -k2n | awk '{OFS="\t";print $1,$2-50,$3+50}' > gencode.exon.pos_add50.bed
bedtools merge -i  gencode.exon.pos_add50.bed > gencode.exon.pos_add50.merge.bed
