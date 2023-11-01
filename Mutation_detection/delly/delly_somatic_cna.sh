/usr/bin/time -v delly cnv -u -z 1000 \
   -o tumor.bcf -c tumor.cov.gz \
   -g /data/database/genome/hg38.fa \
   -m /data/database/delly/mappability_map/Homo_sapiens.GRCh38.dna.primary_assembly.fa.r101.s501.blacklist.gz \
   sampleA.sorted.rmdup.BQSR.bam 
# 53 m, 4.1G

/usr/bin/time -v delly cnv -u \
   -v tumor.bcf \
   -o control.bcf \
   -g /data/database/genome/hg38.fa \
   -m /data/database/delly/mappability_map/Homo_sapiens.GRCh38.dna.primary_assembly.fa.r101.s501.blacklist.gz \
   control_sample.sorted.rmdup.BQSR.bam
# 23m,2.9G

bcftools merge -m id -O b \
   -o tumor_control.bcf \
   tumor.bcf control.bcf >step3.log

bcftools index tumor_control.bcf 

/usr/bin/time -v delly classify -p -f somatic \
   -o somatic.bcf \
   -s samples.tsv \
   tumor_control.bcf 

bcftools query -s sampleA \
   -f "%CHROM\t%POS\t%INFO/END\t%ID\t[%RDCN]\n" \
   somatic.bcf > segmentation.bed

Rscript R/rd.R tumor.cov.gz segmentation.bed 
