# pip install igv-reports==1.9.1 # 1.14.1 有问题
# samtools index wsl1.sorted.markdup.bam

create_report  \
        sites.bed \
        --fasta target_chr.fa \
        --tracks wsl1.sorted.markdup.bam \
        --output examples.html
