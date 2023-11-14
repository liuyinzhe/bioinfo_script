/usr/bin/time -v /data/software/msisensor2-master/msisensor2 msi \
  -c 20 \
  -d hg19.microsatelittes.site  \
  -t tumor.sorted.markdup.BQSR.bam \
  -n normal.sorted.markdup.BQSR.bam \
  -o tumor  >log 2>msisensor2.sum

#-c   <int>      coverage threshold for msi analysis, WXS: 20; WGS: 15, default=20
