# pip install igv-reports
# samtools index wsl1.sorted.markdup.bam

create_report  \
        sites.bed \
        --fasta target_chr.fa \
        --tracks wsl1.sorted.markdup.bam \
        --output examples.html
