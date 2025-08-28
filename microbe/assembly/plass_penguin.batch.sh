#!/bin/bash
cd /data/project/assembly/03.penguin/
if [[ -f /data/project/assembly/shell/penguin.sh.done ]]; then
  echo "文件存在"
else
  rm -rf /data/project/assembly/shell/penguin.sh
  while read sample ; do 
  mkdir -p ${sample}
  echo -e "cd /data/project/assembly/03.penguin ; \
  export PATH=/data/software/plass/bin:\$PATH;\
  /data/software/plass/bin/penguin guided_nuclassemble \
   --threads  10 \
  /data/project/assembly/01.qc/${sample}/${sample}.1.fq.gz \
  /data/project/assembly/01.qc/${sample}/${sample}.2.fq.gz \
 /data/project/assembly/03.penguin/${sample}/assembly.fas \
 /data/project/assembly/03.penguin/${sample} && \
  touch ${sample}.penguin.done " >> /data/project/assembly/shell/penguin.sh

  done < /data/project/assembly/rawdata/sample.lst

  /data/software/miniconda3/bin/paralleltask \
    --disable_convert_path \
    -t local \
    --shell /bin/bash \
    --maxjob 5 \
    -l 1   \
    --job_prefix PenguiN \
    /data/project/assembly/shell/penguin.sh 
fi

if [ $? -eq 0 ];then 
touch /data/project/assembly/shell/penguin.task.sh.done
fi
