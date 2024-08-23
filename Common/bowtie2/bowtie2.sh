rRNA_index = /data/database/rRNA_index
rawdata = /data/rawdata
sample = sampleX
 bowtie2 \
    -x ${rRNA_index} \
    -1 ${rawdata}/${sample}/${sample}.clean.1.fq.gz  \
    -2 ${rawdata}/${sample}/${sample}.clean.2.fq.gz  \
    -S ${sample}_rRNA_bowtie.sam    \
    -p 4 \
    --sensitive \
    --no-unal \
    --un-conc-gz ${sample}_unmap  2> ${sample}.summary
