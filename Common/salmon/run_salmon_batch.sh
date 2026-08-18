#!/bin/bash

work_dir=/ssd/project/NGS/PJ
salmon_index=/ssd/databases/human/salmon_index
export PATH=/data/home/liuyinzhe/binary:$PATH
source /ssd/envs/conda_initialize.sh
conda activate /ssd/envs/NGS
cd ${work_dir}/06.salmon && rm -rf batch_salmon.sh

while read sample ; do
echo -e "cd ${work_dir}/06.salmon && salmon quant \
    -i ${salmon_index} \
    -l A \
    -1 ${work_dir}/rawdata/${sample}.R1.fq.gz \
    -2 ${work_dir}/rawdata/${sample}.R2.fq.gz \
    -o ${sample} \
    --gcBias \
    --seqBias \
    --validateMappings \
    -p 8" >> batch_salmon.sh 
done<${work_dir}/rawdata/sample.lst
cat batch_salmon.sh | parallel -j 8
conda deactivate
