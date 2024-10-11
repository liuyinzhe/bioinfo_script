thread = 12
task_id=project10
query=read.fq.gz
reference=ref.fa
out_bam=sample.sorted.bam
ngmlr -t ${thread} --skip-write -x ont -r ${reference} -q ${query} | \
samtools sort -@ ${thread} -T tmp_$task_id -o ${out_bam} -  >log 2>err



#    -x <pacbio, ont>,  --presets <pacbio, ont>
#        Parameter presets for different sequencing technologies [pacbio]
