cd /data/project/assembly/virus/SPAdes
/data/software/miniconda3/bin/python3 \
 /data/software/SPAdes-3.15.5-Linux/bin/spades.py  \
  -s /data/project/assembly/virus/rawdata/all.fastq.gz \
  --corona \
  --only-assembler \
  -o /data/project/assembly/virus/SPAdes/result
  #-k 21,23,25,27,29,31,33 \
