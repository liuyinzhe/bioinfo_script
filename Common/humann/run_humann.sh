# install
mamba create -y -n humann3 humann   python==3.9
conda activate /data/software/miniconda3/envs/humann3
pip install humann
pip install metaphlan

# run
export PATH=/data/software/miniconda3/envs/humann3/bin:/data/software/miniconda3/envs/humann3/lib/python3.9/site-packages/metaphlan/utils:$PATH
export PYTHONPATH=/data/software/miniconda3/envs/humann3/lib/python3.9/site-packages

cd /data/test/humann/
#humann --help
humann --threads 18 \
  --input sample.fq.gz \
  --input-format fastq.gz \
  --output sample  \
  --metaphlan-options "--bowtie2db /data/database/metaphlan_databases --index mpa_vJun23_CHOCOPhlAnSGB_202307 -t rel_ab"
