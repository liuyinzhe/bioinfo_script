# nohup sh update_clingen.sh &
python3 ClassifyCNV.py \
   --infile Examples/ACMG_examples.hg19.bed \
   --GenomeBuild hg19 \
   --precise \
   --outdir ./xxx && \
cut -f 1-7,43-  ./xxx/Scoresheet.txt > ClassifyCNV_ann.tsv

# input.bed
# chromosome
# CNV start position
# CNV end position
# CNV type (DEL or DUP)

# score:
# ≤ −0.99:   benign variant
# −0.90 .. −0.98:   likely benign variant
# −0.89 .. 0.89:   variant of uncertain significance
# 0.90 .. 0.98:   likely pathogenic variant
# ≥ 0.99:   pathogenic variant
