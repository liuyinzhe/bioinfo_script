reference=hg38.fa
name=AAAAA
fq1=${name}_1.clean.fq.gz
fq2=${name}_2.clean.fq.gz
bwa mem -t 10 -R "@RG\tPU:"${name}"\tID:"${name}"\tSM:"${name}"\tLB:WGS\tPL:ILLUMINA" $reference $fq1 $fq2 | \
sambamba view -t 10 -f bam -S /dev/stdin -o /dev/stdout | sambamba sort -t 10 /dev/stdin -o /dev/stdout | sambamba markup -r -t 10 /dev/stdin -o ${name}.sorted.rmdup.bam
