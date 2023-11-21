#homo_sapiens_hg19#hg38
tracy decompose \
    --annotate homo_sapiens_hg19 \
    --genome /data/public/database/genome/human/hg19/ucsc/hg19.fa.gz \
    --trimLeft  50  \
    --trimRight 50  \
    --callVariants \
    --kmer  15 \
    --support 3 \
    --maxindel 1000 \
    --pratio 0.330000013 \
    --linelimit 60 \
    --outprefix sample.forward \
    sample.forward.ab1

  tracy decompose \
    --annotate homo_sapiens_hg19 \
    --genome /data/public/database/genome/human/hg19/ucsc/hg19.fa.gz \
    --trimLeft  50  \
    --trimRight 50  \
    --callVariants \
    --kmer  15 \
    --support 3 \
    --maxindel 1000 \
    --pratio 0.330000013 \
    --linelimit 60 \
    --outprefix sample.reverse \
    sample.reverse.ab1

bcftools norm -O b -o sample.forward.norm.bcf -f /data/public/database/genome/human/hg19/ucsc/hg19.fa.gz sample.forward.bcf
bcftools norm -O b -o sample.reverse.norm.bcf -f /data/public/database/genome/human/hg19/ucsc/hg19.fa.gz sample.reverse.bcf
bcftools index sample.forward.norm.bcf 
bcftools index sample.reverse.norm.bcf 

bcftools merge -Oz -o  sample.vcf.gz --apply-filters "PASS" --force-samples sample.forward.norm.bcf sample.reverse.norm.bcf
bcftools index sample.vcf.gz
