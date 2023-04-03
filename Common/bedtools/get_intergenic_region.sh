#zcat GCF_001433935.1_IRGSP-1.0_genomic.gtf.gz | grep -v "^#" | cut -f3 | sort | uniq -c | sort -k1rn


#基因间区
genomefile=GCF_902167145.genomic.fna
gtf_gz=GCF_902167145.1gtf.gz
samtools faidx ${genomefile}
awk '{print $1, $2}' ${genomefile}.fai | sed -e 's/ /\t/g' >genome.bed

zcat ${gtf_gz} | awk 'BEGIN{OFS="\t";} $3=="gene" {print $1,$4-1,$5}' >gene.bed
sort -k1V -k2n gene.bed >gene.sorted.bed
sort -k1V -k2n genome.bed > genome.sorted.bed
cat  gene.sorted.bed |complementBed -i stdin -g  genome.sorted.bed  >intergenic_region.bed

#https://zhuanlan.zhihu.com/p/52322803
