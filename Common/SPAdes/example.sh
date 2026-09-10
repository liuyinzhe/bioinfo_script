#!/bin/bash

source /data/home/envs/conda_initialize.sh
conda activate /data/home/envs/spades

work_dir=/data/home/project/assembly/DS26XM109
export PATH=/data/home/binary:$PATH
mode_type=metaviral
mkdir -p ${work_dir}/${mode_type}
cd ${work_dir}/${mode_type}
rm -rf batch_spades.sh
while read sample group ; do
mkdir -p ${work_dir}/${mode_type}/${sample}

echo -e "cd ${work_dir}/${mode_type}/${sample} && \
/data/home/envs/spades/bin/python3 \
/data/home/envs/spades/bin/spades.py \
  --threads 12 \
  --memory 190 \
  -1 ${work_dir}/rawdata/${sample}.1.fq.gz \
  -2 ${work_dir}/rawdata/${sample}.2.fq.gz \
  --${mode_type} \
  -o ${work_dir}/${mode_type}/${sample}" >> batch_spades.sh
done < ${work_dir}/rawdata/sample.lst
cat batch_spades.sh | parallel -j 1

conda deactivate
