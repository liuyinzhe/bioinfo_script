/home/software/isONclust3 \
   -k 13  -w 51 -s 9  -t 3 \
   --min-shared-minis 0.5 \
   --fastq input.fastq \
   --outfolder ${PWD} \
   --mode pacbio

#--no-fastq 不输出分组的fastq

# 默认值
#n: 1
#outfolder "/data/isONclust"
#k: 15
#w: 51
#s: 9
#t: 3
#quality_threshold 0.7385691026454038
#Min shared minis: 0.5
