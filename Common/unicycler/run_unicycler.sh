
# ngs PE
sample=sample
export PATH=/data/envs/unicycler/bin:$PATH;
cd /data/project/assembly/unicycler
unicycler \
 --min_fasta_length 500 \
 -1 /data/project/assembly/unicycler/01.qc/${sample}/${sample}.1.fq.gz \
 -2 /data/project/assembly/unicycler01.qc/${sample}/${sample}.2.fq.gz \
 -t 10 \
 -o /data/project/assembly/unicycler/02.assembly/${sample} 
