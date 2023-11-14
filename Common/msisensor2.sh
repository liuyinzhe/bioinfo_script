# /data/software/msisensor2-master/msisensor2 scan \
 # -d /data/database/genome/human_hg19/hg19.fa \
 # -o hg19.microsatelittes.site

# ln -s /data/home/liuyinzhe/software/msisensor2-master/models_hg19_GRCh37 .
/usr/bin/time -v /data/home/liuyinzhe/software/msisensor2-master/msisensor2 msi \
  -d hg19.microsatelittes.site  \
  -t tumor.sorted.markdup.BQSR.bam \
  -n normal.sorted.markdup.BQSR.bam \
  -o tumor  >log 2>msisensor2.sum
