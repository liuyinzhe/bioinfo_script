thread=12
task_id=project10
query=read.fq.gz
reference=ref.fa
out_bam=sample.sorted.bam
minimap2 -t ${thread} -L --MD -Y -a -x map-pb ${reference} ${query} | \
    samtools sort -@ ${thread} -T tmp_$task_id -o ${out_bam} - >log 2>err


#  Preset:
#    -x STR       preset (always applied before other options; see minimap2.1 for details) []
#                 - map-pb/map-ont - PacBio CLR/Nanopore vs reference mapping
#                 - map-hifi - PacBio HiFi reads vs reference mapping
#                 - ava-pb/ava-ont - PacBio/Nanopore read overlap
#                 - asm5/asm10/asm20 - asm-to-ref mapping, for ~0.1/1/5% sequence divergence
#                 - splice/splice:hq - long-read/Pacbio-CCS spliced alignment
#                 - sr - genomic short-read mapping
