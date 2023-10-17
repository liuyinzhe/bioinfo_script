/data/software/qualimap_v2.3/qualimap  bamqc \
  -bam sample.sorted.markdup.bam \
  --genome-gc-distr hg38 \
  --collect-overlap-pairs \
  -outformat PDF:HTML \
  -outdir ${PWD}/qualimap_report \
  -nt 8 \
  --java-mem-size=10G 
