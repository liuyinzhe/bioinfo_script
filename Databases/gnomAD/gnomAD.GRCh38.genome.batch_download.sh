#!/usr/bin/env bash
set -euo pipefail

# ---- 参数解析 ----
if [[ $# -lt 2 ]]; then
  echo "用法: $0 [aws|gcp] [输出目录]" >&2
  exit 1
fi

SOURCE="$1"
OUTDIR="$2"

LIST="${OUTDIR}/urls_${SOURCE}.txt"

case "$SOURCE" in
  aws)
    BASE="https://gnomad-public-us-east-1.s3.amazonaws.com/release/4.1.1/vcf/genomes"
    ;;
  gcp)
    BASE="https://storage.googleapis.com/gcp-public-data--gnomad/release/4.1.1/vcf/genomes"
    ;;
  *)
    echo "用法: $0 [aws|gcp] [输出目录]" >&2
    exit 1
    ;;
esac

mkdir -p "$OUTDIR"
: > "$LIST"

chroms=(chr{1..22} chrX chrY)
exts=(.vcf.bgz .vcf.bgz.tbi)

for chr in "${chroms[@]}"; do
  for ext in "${exts[@]}"; do
    fname="gnomad.genomes.v4.1.1.sites.${chr}${ext}"
    echo "${BASE}/${fname}" >> "$LIST"
  done
done

echo "URL 列表已生成: $LIST"
echo "开始批量下载..."
aria2c -c -x 8 -s 4 -k 1M \
  --retry-wait=5 --max-tries=5 \
  -j 4 -d "$OUTDIR" -i "$LIST"

echo "全部完成。文件在: $OUTDIR"
