gatk BedToIntervalList \
    -I S07604514_Covered.bed \
    -O bait.hg38.covered.interval_list \
    -SD /data/database/genome/hg38/hg38.dict
# 常用 目标区域 + 侧翼扩展区间
gatk BedToIntervalList \
    -I S07604514_Padded.bed \
    -O target.hg38.padded.interval_list \
    -SD /data/database/genome/hg38/hg38.dict
# 严格的目标区域
gatk BedToIntervalList \
    -I S07604514_Regions.bed \
    -O target.hg38.regions.interval_list \
    -SD /data/database/genome/hg38/hg38.dict
