# pip install igv-reports==1.9.1 # 1.14.1 有问题
# samtools index wsl1.sorted.markdup.bam

create_report  \
        sites.bed \
        --fasta target_chr.fa \
        --tracks wsl1.sorted.markdup.bam \
        --output examples.html

#bed文件需要有后缀,只识别文件后缀
#TAX2    0       996     TAX2:1-996

create_report  \
     sample.bed  \
     --standalone \
     --fasta  /data/home/liuyinzhe/project/WGS/DS2026YW08_s/ref/TAX2.fa \
     --tracks DC-BK26-E10-MCB20260509.bam  DC-BK26-E10-WCB20260609-D15.bam  IR-DC-BK26-E10-WCB20260624.bam \
     --output examples.html

#
create_report test/data/variants/variants.vcf.gz \
--genome hg38 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--tracks test/data/variants/variants.vcf.gz test/data/variants/recalibrated.bam \
--title "IGV Variant Inspector" \
--output example_vcf.html

#https://github.com/igvteam/igv-reports/blob/master/test/example_footer.html
# example
# https://igvteam.github.io/igv-reports/
