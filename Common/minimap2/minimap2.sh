thread=12
task_id=project10
query=read.fq.gz
reference=ref.fa
out_bam=sample.sorted.bam
minimap2 -t ${thread} -L --MD -Y -a -x map-pb ${reference} ${query} | \
    samtools sort -@ ${thread} -T tmp_$task_id -o ${out_bam} - >log 2>err
