#!/bin/bash
project_dir=/data/project_id
cd ${project_dir}/bwa/assembly
/data/envs/microbe/bin/spades.py \
  -1 ${project_dir}/bwa/reads/sample.1.fq \
  -2 ${project_dir}/bwa/reads/sample.2.fq \
  --rnaviral \
  --threads 16 \
  --memory 100 \
  --checkpoints last \
  -o ${project_dir}/bwa/assembly/result 
 # --continue  \

 # 非corona的RNA病毒,组装效果 rnaviral > corona
