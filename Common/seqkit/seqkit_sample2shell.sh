rm -rf batch_seqkit_sample.sh
mkdir -p sample
while read sample ;do

 echo -e "seqkit sample  \
 --rand-seed 123 \
 --proportion 0.9 \
 ${sample}.1.fq.gz  |seqkit head -n 5000  |gzip > sample/${sample}.1.fq.gz 
seqkit sample  \
 --rand-seed 123 \
 --proportion 0.9 \
 ${sample}.2.fq.gz  |seqkit head -n 5000  |gzip > sample/${sample}.2.fq.gz  " >> batch_seqkit_sample.sh

done <sample.lst

# nohup cat batch_seqkit_sample.sh  |parallel  -j 4  &
