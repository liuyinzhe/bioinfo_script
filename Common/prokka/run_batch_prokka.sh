#!/bin/bash
project_dir=/data3/cmseq
kingdom=Bacteria
cd ${project_dir}/prokka
if [[ -f ${project_dir}/shell/prokka.sh.done ]]; then
  echo "文件存在"
else
  rm -rf ${project_dir}/shell/prokka.sh
  while read sample ; do 
  echo -e "export PATH=/data/binary:/data/envs/microbe/bin:\$PATH; ulimit -HSn 4096 ; \
  cd ${project_dir}/prokka/${sample} ; \
  prokka \
    ${project_dir}/megahit/${sample}/final.contigs.fa \
    --outdir ${project_dir}/prokka/${sample}/ \
    --prefix ${sample} \
    --kingdom ${kingdom} && touch ${sample}.prokka.done" >> ${project_dir}/shell/prokka.sh
  done < ${project_dir}/rawdata/sample.lst

  /data/software/miniconda3/bin/paralleltask \
    --disable_convert_path \
    -t local \
    --shell /bin/bash \
    --maxjob 20 \
    -l 1   \
    --job_prefix prokka \
    ${project_dir}/shell/prokka.sh
fi

if [ $? -eq 0 ];then 
touch ${project_dir}/shell/prokka.task.sh.done
fi
