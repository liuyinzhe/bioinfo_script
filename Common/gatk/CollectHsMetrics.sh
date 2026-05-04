sample=$(echo $(basename $PWD))
gatk CollectHsMetrics \
    -I ${sample}.sorted.markdup.BQSR.bam \
    -O ${smaple}.metrics.txt \
    -R /data/home/liuyinzhe/database/genome/bwamem2/hg38.fa \
    --BAIT_INTERVALS /data/database/genome/human_hg38/bait.hg38.covered.interval_list \
    --TARGET_INTERVALS /data/database/genome/human_hg38/target.hg38.padded.interval_list 
