# pip install igv-reports

create_report  \
        sites.bed \
        --fasta target_chr.fa \
        --tracks wsl1.sorted.markdup.bam \
        --output examples.html
