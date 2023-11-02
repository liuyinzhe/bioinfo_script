#!/bin/bash

cd /data/emapper_annotations/
mkdir -p output
unset PYTHONPATH
/data/bin/emapper.py \
 -m diamond \
 -i GCFxxx_protein.faa  \
 --itype proteins \
 --cpu 30 \
 --output_dir /data/emapper_annotations/output \
 --excel \
 -o sample  >/data/emapper_annotations/log 2>/data/emapper_annotations.err 

 # 覆盖之前结果
 # Resumes a previous emapper run, skipping results in existing output files.
 #--resume  \
