/usr/bin/time -v /data/software/msisensor2-master/msisensor2 msi \
  -d hg19.microsatelittes.site  \
  -t tumor.sorted.markdup.BQSR.bam \
  -n normal.sorted.markdup.BQSR.bam \
  -o tumor  >log 2>msisensor2.sum
