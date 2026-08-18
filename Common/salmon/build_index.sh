# cds_extract
#gffread GRCh38.gtf -g GRCh38.fa -x GRCh38.cds.fa
/ssd/binary/gffread \
   /ssd/databases/MANE_human/v1.5/MANE.GRCh38.v1.5.ensembl_genomic.rename.gtf \
   -g /ssd/databases/human/GRCh38.fa \
   -x GRCh38_cds.fa 

# build_decoy_aware_index
# 准备 decoy 列表
grep "^>" GRCh38.fa | cut -d " " -f 1 | sed 's/>//g' > decoys.txt

# 拼接 转录组 + 基因组
#cat Homo_sapiens.GRCh38.cdna.all.fa GRCh38.fa > gentrome.fa
cat GRCh38_cds.fa GRCh38.fa > gentrome.fa

# 构建 decoy-aware 索引
salmon index -t gentrome.fa -d decoys.txt -i salmon_index -p 8
