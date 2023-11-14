/data/envs/Common/bin/msisensor-pro msi \
  -c  20 \
  -d  ./hg19.microsatelittes.site  \
  -t SP42.sorted.markdup.BQSR.bam \
  -n PC_41.sorted.markdup.BQSR.bam \
  -o tumor

  # -c   <int>      coverage threshold for msi analysis, WXS: 20; WGS: 15, default=15
