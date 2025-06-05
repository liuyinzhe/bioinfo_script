
ls *.fasta |awk -F"." '{print $1"\t"$1}' >labels.tab
touch classes.tab

export PATH=/data/software/miniconda3/envs/pyani:$PATH;
  /data/software/miniconda3/envs/pyani/bin/python  \
 /data/software/miniconda3/envs/pyani/bin/average_nucleotide_identity.py \
  -f \
  -i /data/project/assembly/03.pyani \
  -o /data/project/assembly/03.pyani/ANIb_output/ \
  -g --gformat png \
  --classes /data/project/assembly/03.pyani/classes.tab \
  --labels /data/project/assembly/03.pyani/labels.tab \
   -m ANIb --gmethod seaborn 
