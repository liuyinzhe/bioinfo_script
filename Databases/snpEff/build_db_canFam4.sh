#!/bin/bash
# =============================================================================
# 用法: bash scripts/build_db_canFam4.sh
# 日志: $SNPEFF_HOME/log_canFam4.build
# =============================================================================
set -euo pipefail
# 0) 配置snpEff.config
cat <<'EOF' >> snpEff.config
# Canis lupus familiaris (dog) - NCBI UU_Cfam_GSD_1.0 / GCF_011100685.1, name canFam4
canFam4.genome : Canis_lupus_familiaris
canFam4.reference : /data/public/databases/genomes/Canis_lupus/canFam4
EOF


SNPEFF_HOME=/data/public/software/snpEff
JAVA=/data/public/software/jdk-21.0.12.1/bin/java
GFFREAD=/data/public/env/rna_seq/bin/gffread
SRC=/data/public/databases/genomes/Canis_lupus/canFam4
GENOME=canFam4
FA_GZ=$SRC/GCF_011100685.1_UU_Cfam_GSD_1.0_genomic.fna.gz
GFF_GZ=$SRC/GCF_011100685.1_UU_Cfam_GSD_1.0_genomic.gff.gz
GTF_GZ=$SRC/GCF_011100685.1_UU_Cfam_GSD_1.0_genomic.gtf.gz
WORK=/tmp/snpeff_build                       # 解压大文件的临时目录 (/ 有空间)
DATA=$SNPEFF_HOME/data/$GENOME

mkdir -p "$DATA" "$SNPEFF_HOME/data/genomes" "$WORK"

# 1) 参考基因组: 软链接, snpEff 可直接读 .gz
ln -sf "$FA_GZ" "$SNPEFF_HOME/data/genomes/$GENOME.fa.gz"

# 2) 基因注释: GTF (SnpEff 首选格式)
ln -sf "$GTF_GZ" "$DATA/genes.gtf.gz"

# 3) cds.fa / protein.fa: build 时用于自检, 由 GFF3 + 基因组经 gffread 提取
if [ ! -s "$DATA/protein.fa.gz" ]; then
    [ -s "$WORK/$GENOME.fa" ] || zcat "$FA_GZ" > "$WORK/$GENOME.fa"
    gzip -dc "$GFF_GZ" | "$GFFREAD" -g "$WORK/$GENOME.fa" \
        -y "$WORK/$GENOME.protein.fa" -x "$WORK/$GENOME.cds.fa" - \
        > "$WORK/gffread.$GENOME.log" 2>&1
    # 去掉 NCBI 的 "rna-" 前缀, 让 FASTA 头与 GTF 的 transcript_id 完全一致
    sed -i 's/^>rna-/>/' "$WORK/$GENOME.protein.fa" "$WORK/$GENOME.cds.fa"
    gzip -c "$WORK/$GENOME.protein.fa" > "$DATA/protein.fa.gz"
    gzip -c "$WORK/$GENOME.cds.fa"     > "$DATA/cds.fa.gz"
fi

# 4) 构建数据库 (需先在 snpEff.config 中登记 canFam4.genome,已完成)
cd "$SNPEFF_HOME"
"$JAVA" -Xms2g -Xmx32g -jar snpEff.jar build -gtf22 -v "$GENOME" \
    > "$SNPEFF_HOME/log_$GENOME.build" 2>&1

# 5) 自检结果摘要
grep -E "^(CDS check|Protein check|Number of|Genes|Transcripts)" "$SNPEFF_HOME/log_$GENOME.build" | tail -20 || true
ls -l "$DATA"
echo "OK: $GENOME"
