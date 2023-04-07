# 挑选exon 坐标,保留基因名 gene_name (gene symbol)，带引号，如 "TP53"
zcat gencode.v42.annotation.gtf.gz  |grep -v "^#" | awk '$3=="exon"{print }' |cut -f 1,2,4,5,7,9 |cut -d";"  -f 1,2,3,4 | awk -F" " 'BEGIN{OFS="\t";}{print $1,$3,$4,$5,$13}' > gencode.exon.bed
# 使用目标基因名筛选， -w 尽可能保证全词匹配，但是遇到带破折号 - 的会也匹配出来
# 所以基因ID 是带引号的如 "TP53" 可以避免这种情况
grep -w -f num_gene.g.lst  gencode.exon.bed >gencode.num.gene.exon.bed

# 排序去重(单独行完全一样的)，坐标进行排序，使用bedtools merge 功能，将坐标进行合并，重叠的坐标生成一个更大的区间坐标
cut -f 1,2,3 gencode.num.gene.exon.bed |sort -u |sort -u -k1V -k2n -k3n | bedtools merge -i - > exon.bed

# 统计 涉及到的基因 exon 中长度，计算panel 大小
awk 'BEGIN{a=0}{a+=$3-$2+1;}END{print a;}' exon.bed  
#1518451
# 同上，不过gencode.num.gene.exon.bed  是没有进行坐标去重，合并操作的，所以更大
awk 'BEGIN{a=0}{a+=$3-$2+1;}END{print a;}' gencode.num.gene.exon.bed  
#7474659
