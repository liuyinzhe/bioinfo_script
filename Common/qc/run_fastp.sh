#!/bin/bash

sample=A
mkdir -p ${sample}
/data/envs/Common/bin/fastp \
  --in1 ../../rawdata/${sample}.1.fq.gz \
  --in2 ../../rawdata/${sample}.2.fq.gz \
  --out1 ${sample}/${sample}.clean.1.fq.gz \
  --out2 ${sample}/${sample}.clean.2.fq.gz \
  --json ${sample}/${sample}.fastp.json \
  --html ${sample}/${sample}.qc.html \
  --trim_poly_g \
  --trim_poly_x \
  --low_complexity_filter \
  --correction \
  --report_title  '${sample}' \
  --thread 8 >${sample}/${sample}.log \
  2>${sample}/${sample}.err && \
  touch ${sample}.done 



#--trim_poly_g
#--poly_g_min_len       10

#--trim_poly_x
#--poly_x_min_len       10

#--low_complexity_filter
#--complexity_threshold 30

#--correction
#--overlap_len_require  30
#--overlap_diff_limit   5
#--overlap_diff_percent_limit 20
