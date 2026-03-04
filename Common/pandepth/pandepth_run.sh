# regions
pandepth \
 -i sample.bam \
 -b Regions.sorted.merge.bed  \
 -o sample_prefix

# chrs
 pandepth \
  -i sample.bam \
  -o sample_prefix

samtools stats sample.bam > sample.stat 
