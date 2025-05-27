export PATH=/data/envs/getorganelle/bin:$PATH;

cd /data/project/assembly/GetOrganelle/sample/Q

sample="Q"
forward_fq="Q_R1.fq"
reverse_fq="Q_R2.fq"

get_organelle_from_reads.py \
  -t 20 \
  -1 ${forward_fq} \
  -2 ${reverse_fq} \
  -R 10 -k 21,45,65,85,105 \
  -F animal_mt -o ${sample}
