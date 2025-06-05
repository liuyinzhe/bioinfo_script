#!/bin/bash
cd /data/project/assembly/02.GetOrganelle/
if [[ -f /data/project/assembly/shell/GetOrganelle.sh.done ]]; then
  echo "文件存在"
else
  rm -rf /data/project/assembly/shell/GetOrganelle.sh
  while read sample ; do 
  #mkdir -p ${sample}
  echo -e "cd /data/project/assembly/02.GetOrganelle ; \
  export PATH=/data/envs/getorganelle/bin:\$PATH;\
  zcat /data/project/assembly/01.qc/${sample}/${sample}.clean.1.fq.gz > /data/project/assembly/02.GetOrganelle/${sample}.forward.1.fq && \
  zcat /data/project/assembly/01.qc/${sample}/${sample}.clean.2.fq.gz > /data/project/assembly/02.GetOrganelle/${sample}.reverse.2.fq && \
  get_organelle_from_reads.py \
    -t 10 \
    -1 ${sample}.forward.1.fq \
    -2 ${sample}.reverse.2.fq \
    -R 10 -k 21,45,65,85,105 \
    -F animal_mt -o ${sample} && \
    touch ${sample}.GetOrganelle.done " >> /data/project/assembly/shell/GetOrganelle.sh

  done < /data/project/assembly/rawdata/sample.lst

  /data/software/miniconda3/bin/paralleltask \
    --disable_convert_path \
    -t local \
    --shell /bin/bash \
    --maxjob 5 \
    -l 1   \
    --job_prefix GetOrganelle \
    /data/project/assembly/shell/GetOrganelle.sh 
fi

if [ $? -eq 0 ];then 
touch /data/project/assembly/shell/GetOrganelle.task.sh.done
fi


#    rm -rf ${sample}.forward.1.fq ${sample}.reverse.2.fq && \


